from syndata import SynDataGenerator

def uni_dropouts():
     return (
        SynDataGenerator()
        .addString("sex", ["male", "female"], [0.412, 0.588])
        .addString("employment", ["employed", "unemployed"])
        .addFloat("gpa", 1.0, 4.0, 1)
        .addInt("years", 1, 8)
        .addString("degree level", ["bachelors","masters","doctorate"])
        .addString("degree field", ["computer science","art history","english literature","pre law","pre medicine"])
        .addString("completion", ["completed", "dropped out"])
        .addCorruptCells([0.05]*7)
        .addBlankCells([0.2]*7)
        )

def patients():
    return (
        SynDataGenerator()
        .addIndex("ID")
        .addString("First Name", ["Allen","Bary","Christine","Dana","Elena","Francis","Gary"])
        .addString("Last Name",["Zelena","Yana","Xander","Willian","Vader","Umber","Thesius"])
        .addString("Insurance",["Cigna","Aetna","Kaiser"])
        .addInt("weight",100, 300)
        .addFloat("height", 4.0, 6.5, 1)
        )

def main():
    uni_dropouts().dumpCSV("data.csv", 100)
    patients().dumpTXT("patients.txt", 100, ['|']*5+[''])

if __name__ == "__main__":
    main()