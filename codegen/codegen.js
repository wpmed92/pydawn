const { parse, write, validate } = require("webidl2");
const fs = require('fs');

const webgpuIdlString = fs.readFileSync("./webgpu.idl", 'utf8');
const tree = parse(webgpuIdlString);
let classes = ""
let indent = 0;


function printIndent() {
    for (let i = 0; i < indent; i++) {
        classes += " ";
    }
}

for (const astNode of tree) {
    console.log(astNode.type);

    if (astNode.type == "interface") {
        classes += "\nclass " + astNode.name + ":\n";
        console.log("INTERFACE: " + astNode.name);
        console.log("--------------------------")
        let opOrConstr = false;
        for (const member of astNode.members) {
            console.log(member.type)
            if (member.type == "attribute") {
                console.log("   ATTRIBUTE: " + member.name)
                console.log("   --------------------------")
            }
            if (member.type == "operation") {
                console.log("   OPERATION: " + member.name)
                console.log("   --------------------------")
                classes += "  def " + member.name + "(self";
                opOrConstr = true;

                for (const argument of member.arguments) {
                    console.log("     arg: " + argument.name)
                    classes += ", " + argument.name;
                }

                classes += "):\n"
                classes += "    pass\n";
            }
            if (member.type == "constructor") {
                opOrConstr = true;
                console.log("   CONSTRUCTOR")
                console.log("   --------------------------")
                classes += "  def __init__(self";
                selfAssigns = "";
                for (const argument of member.arguments) {
                    console.log("     arg: " + argument.name)
                    classes += "," + argument.name;
                    selfAssigns += "      self." + argument.name + " = " + argument.name + "\n";
                }
                classes += "):\n";
                classes += selfAssigns;
            }
        }
        if (!opOrConstr) {
            classes += "  pass\n";
        }
        console.log("INHERITANCE")
        console.log(astNode.inheritance)
    }
    //console.log(astNode.name);
}
fs.writeFileSync("classes.py", classes, { encoding: "utf-8" });
const text = write(tree);
const validation = validate(tree);