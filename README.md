# KNOX-SmartLinker
Tool that links an ontologys classes to a fitting definition from DBPedia. This tool was made for the AAU KNOX super project, specifically the medical preprocessing layer.

## Dependencies
- SPARQLWrapper
    - To install use: `pip install SPARQLWrapper`

## Usage
Running the tool: <br>
`SmartLinker.py INPUT_PATH`

Here `INPUT_PATH` is the path to the ontology file you want to link.

When the tool has run, a new file titled `Linked_'INPUT_PATH'` will be created next to the original file. This is the linked ontology.
<br><br>

**IMPORTANT:**<br>
Make sure the input ontology has a **newline** between the class definition and the rdf:type. <br>
Ex: 
```
:Hospital
    rdf:type owl:Class ;
```
If this is **NOT** the case, you can utilize the `-i` flag (Example in *Optional Flags* section).


### Optional Flags
- `-h`
    - Describes how to use the tool, and what flags exist.
- `-i`
    - Use this flag if your owl:class is on the same line as the class definition.<br>Ex: `:Hospital rdf:type owl:Class ;`