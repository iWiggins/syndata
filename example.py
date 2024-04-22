from syndata import SynDataGenerator

def main(): (
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
        .dump("data.csv", 100)
        )

if __name__ == "__main__":
    main()