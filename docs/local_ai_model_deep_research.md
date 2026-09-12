root ::= InstaGraph
InstaGraph ::= "{\n" "  \"nodes\": " NodeList ",\n" "  \"edges\": " EdgeList "\n}"
NodeList   ::= "[" (Node (",\n" Node)*)? "]"
Node       ::= "{\n" "    \"id\": " String ",\n" "    \"label\": " String ",\n" "    \"verbatim_quote\": " String "\n  }"
EdgeList   ::= "[" (Edge (",\n" Edge)*)? "]"
Edge       ::= "{\n" "    \"source\": " String ",\n" "    \"target\": " String ",\n" "    \"category\": " Category ",\n" "    \"description\": " String "\n  }"
Category   ::= "\"Interactivity\"" | "\"Containment\"" | "\"State Change\"" | "\"Reference\""
String     ::= "\"" ([^"\\] | "\\" .)* "\""