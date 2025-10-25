// Simple Rust scanner CLI skeleton (PoC)
// - Multi-threaded file walker (rayon)
// - Filename & content-head heuristics
// - Emits JSONL per hit to stdout
// Comments and names use English conventions as requested.

use clap::Parser;
use rayon::prelude::*;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Read, Write};
use walkdir::WalkDir;
use std::path::PathBuf;
use regex::Regex;
use serde::Serialize;
use sha2::{Digest, Sha256};
use anyhow::Result;

#[derive(Parser, Debug)]
#[command(author, version, about = "rustscanner PoC - filename + head scan")]
struct Args {
  /// Path to case root or mounted image
  #[arg(short, long)]
  root: PathBuf,

  /// Maximum file size to read head (bytes)
  #[arg(short, long, default_value_t = 200_000)]
  head_size: usize,

  /// Number of threads to use (rayon default if omitted)
  #[arg(short, long)]
  threads: Option<usize>,
}

#[derive(Serialize)]
struct Hit {
  case: String,
  path: String,
  filesize: u64,
  pattern: String,
  snippet: String,
  sha256: String,
  timestamp: String,
  scanner_version: String,
}

fn sha256_of_file(path: &PathBuf) -> Result<String> {
  let mut f = File::open(path)?;
  let mut hasher = Sha256::new();
  let mut buf = [0u8; 65536];
  loop {
    let n = f.read(&mut buf)?;
    if n == 0 { break; }
    hasher.update(&buf[..n]);
  }
  Ok(hex::encode(hasher.finalize()))
}

fn read_head(path: &PathBuf, n: usize) -> Result<String> {
  let mut f = File::open(path)?;
  let mut buf = vec![0u8; n];
  let read = f.read(&mut buf)?;
  buf.truncate(read);
  // best-effort UTF-8; fallback to lossy
  Ok(String::from_utf8_lossy(&buf).to_string())
}

fn main() -> Result<()> {
  let args = Args::parse();
  if let Some(t) = args.threads {
    rayon::ThreadPoolBuilder::new().num_threads(t).build_global().ok();
  }

  let filename_patterns = vec![
    Regex::new("(?i)wallet")?,
    Regex::new("(?i)keystore")?,
    Regex::new("(?i)mnemonic")?,
    Regex::new("(?i)seed")?,
    Regex::new("(?i)private.*key")?,
    Regex::new("(?i)ethereum")?,
    Regex::new("(?i)btc")?,
  ];

  let content_patterns = vec![
    Regex::new(r"\"crypto\"\s*:")?,
    Regex::new(r"\"address\"\s*:")?,
    Regex::new(r"[a-f0-9]{64}")?,
    Regex::new(r"([a-z]+(\s+[a-z]+){11,24})")?,
  ];

  let scanner_version = env!("CARGO_PKG_VERSION").to_string();
  let case_id = args.root.to_string_lossy().to_string();
  let walker: Vec<PathBuf> = WalkDir::new(&args.root)
    .follow_links(false)
    .into_iter()
    .filter_map(|e| e.ok())
    .filter(|e| e.file_type().is_file())
    .map(|e| e.into_path())
    .collect();

  walker.par_iter().for_each(|path| {
    // best-effort: skip unreadable files
    let filesize = path.metadata().map(|m| m.len()).unwrap_or(0);
    let filename = path.file_name().and_then(|s| s.to_str()).unwrap_or("").to_string();

    // filename heuristics
    let mut matched = None;
    for p in &filename_patterns {
      if p.is_match(&filename) {
        matched = Some(format!("filename:{}", p.as_str()));
        break;
      }
    }

    // content head heuristics
    if matched.is_none() {
      if let Ok(head) = read_head(path, args.head_size) {
        for p in &content_patterns {
          if p.is_match(&head) {
            matched = Some(format!("content:{}", p.as_str()));
            // mask snippet: for PoC just truncate and replace newlines
            let snippet = head.replace("\n", " ").chars().take(200).collect::<String>();
            if let Ok(sha) = sha256_of_file(path) {
              let hit = Hit {
                case: case_id.clone(),
                path: path.to_string_lossy().to_string(),
                filesize,
                pattern: matched.clone().unwrap_or_default(),
                snippet,
                sha256: sha,
                timestamp: chrono::Utc::now().to_rfc3339(),
                scanner_version: scanner_version.clone(),
              };
              // write JSONL to stdout (best-effort; ignore errors)
              let _ = writeln!(io::stdout(), "{}", serde_json::to_string(&hit).unwrap());
            }
            break;
          }
        }
      }
    } else {
      // filename-based hit: produce small hit object without reading whole file
      let snippet = "[FILENAME MATCH]".to_string();
      if let Ok(sha) = sha256_of_file(path) {
        let hit = Hit {
          case: case_id.clone(),
          path: path.to_string_lossy().to_string(),
          filesize,
          pattern: matched.clone().unwrap_or_default(),
          snippet,
          sha256: sha,
          timestamp: chrono::Utc::now().to_rfc3339(),
          scanner_version: scanner_version.clone(),
        };
        let _ = writeln!(io::stdout(), "{}", serde_json::to_string(&hit).unwrap());
      }
    }
  });

  Ok(())
}