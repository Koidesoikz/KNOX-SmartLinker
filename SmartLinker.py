from argparse import ArgumentParser
from SPARQLWrapper import SPARQLWrapper, JSON

#Reads the given ontology, and returns a list of the lines within the file
#Input: The path to the ontology
def ReadOntology(path):
    with open(f'{path}') as file:
        return file.readlines()

#Returns a list containing the names of all classes in the ontology
#Input: A list of strings, extracted from the ontology
def ExtractClasses(lines):
    classes = []

    for line in lines:
        if "owl:Class" in line:
            classes.append(prevLine.split(" ")[0][1:-1])
        prevLine = line

    return classes

def ExtractClassesInline(lines):
    classes = []

    for line in lines:
        if "owl:Class" in line:
            classes.append(line.split(" ")[0][1:])

    return classes

#Returns the IRI to DBPedias definition of the given classname
#Input: A classname to query
def RunQuery(className):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery('select ?Concept where {?Concept rdfs:label "' + str(className) + '"@en} LIMIT 100')

    #Converts query result to JSON    
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    #Loops through the bindings in the result (Inspired from: https://rebeccabilbro.github.io/sparql-from-python/)
    for hit in result["results"]["bindings"]:
        #Returns the IRI, if it contains the "/resource/" path and isn't a "Category"
        if ("/resource/" in hit["Concept"]["value"]) and not ("Category:" in hit["Concept"]["value"]):
            return hit["Concept"]["value"]

#Adds class definitions to the ontology, and writes the result into a new file
#Input: A dictionary containing the classnames of the ontology, and the IRIs from DBPedia.
#       A path to the input ontology
def WriteLinksInRDF(LinkDict, path):
    lines = ReadOntology(path)
    newContent = ""

    #Loops throug the lines in the ontology, and insert the DBPedia definition where appropriate
    for line in lines:
        if "owl:Class" in line:
            newLine = ""
            splitLine = line.split(" ")

            iri = LinkDict[prevLine.split(" ")[0][1:-1]]

            splitLine[-1] += f"rdfs:isDefinedBy <{iri}>;\n"

            for elem in splitLine:
                newLine += elem + " "
            newContent += newLine
        else:
            newContent += line
        
        prevLine = line

    #Writes the result to a new file, next to the original, called: "'NAME_OF_INPUT_ONTOLOGY'_Linked"

    file = open(path[:-4] + "_Linked.ttl", "w")
    file.write(newContent)
    file.close()

def WriteLinksInRDFInline(LinkDict, path):
    lines = ReadOntology(path)
    newContent = ""

    #Loops throug the lines in the ontology, and insert the DBPedia definition where appropriate
    for line in lines:
        if "owl:Class" in line:
            newLine = ""
            splitLine = line.split(" ")

            iri = LinkDict[line.split(" ")[0][1:]]

            splitLine[-1] += f"rdfs:isDefinedBy <{iri}>;\n"

            for elem in splitLine:
                newLine += elem + " "
            newContent += newLine
        else:
            newContent += line

    #Writes the result to a new file, next to the original, called: "'NAME_OF_INPUT_ONTOLOGY'_Linked"

    file = open(path[:-4] + "_Linked.ttl", "w")
    file.write(newContent)
    file.close()

#The "Main" function
def Main(path, inline):
    try:
        #Extracts a list of classes from the input ontology
        if(inline):
            classes = ExtractClassesInline(ReadOntology(path))
        else:
            classes = ExtractClasses(ReadOntology(path))

        iriDict = {}

        #Querys for the IRIs of all the classes
        for className in classes:
            iriDict[className] = RunQuery(className)
        
        #Adds the class definition to the ontology, and saves it in a new file
        if(inline):
            WriteLinksInRDFInline(iriDict,path)
        else:
            WriteLinksInRDF(iriDict, path)

    #Handles errors
    except Exception as e:
            print("An error has occured")
            print(e)

#Parse the arguments, and runs main when the script is executed
if __name__ == "__main__":
    parser = ArgumentParser(description="This script takes an ontology as input, and links its owl classes to similar classes found in DBPedia. The output of this script will be located next to the input ontology with the name: 'filename'_Linked")
    parser.add_argument('-i', action='store_true', help="Meant for testing purposes. Use this flag, if ontology file has classname on the same line as the rdf:type.")
    parser.add_argument('INPUT_PATH', help="The path to the input ontology")
    args = parser.parse_args()

    Main(args.INPUT_PATH, args.i)