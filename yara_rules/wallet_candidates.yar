rule ethereum_keystore_json
{
  meta:
    description = "Detect ethereum keystore JSON files by presence of \"crypto\" and \"address\" keys"
  strings:
    $a = "\"crypto\"" ascii
    $b = "\"address\"" ascii
  condition:
    $a and $b
}