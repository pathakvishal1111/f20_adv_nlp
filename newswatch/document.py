import spacy

nlp = spacy.load("en_core_web_sm")

sample = """Dollar gains on Greenspan speech

The dollar has hit its highest level against the euro in almost three months after the Federal Reserve head said the US trade deficit is set to stabilise.

And Alan Greenspan highlighted the US government's willingness to curb spending and rising household savings as factors which may help to reduce it. In late trading in New York, the dollar reached $1.2871 against the euro, from $1.2974 on Thursday. Market concerns about the deficit has hit the greenback in recent months. On Friday, Federal Reserve chairman Mr Greenspan's speech in London ahead of the meeting of G7 finance ministers sent the dollar higher after it had earlier tumbled on the back of worse-than-expected US jobs data. "I think the chairman's taking a much more sanguine view on the current account deficit than he's taken for some time," said Robert Sinche, head of currency strategy at Bank of America in New York. "He's taking a longer-term view, laying out a set of conditions under which the current account deficit can improve this year and next."

Worries about the deficit concerns about China do, however, remain. China's currency remains pegged to the dollar and the US currency's sharp falls in recent months have therefore made Chinese export prices highly competitive. But calls for a shift in Beijing's policy have fallen on deaf ears, despite recent comments in a major Chinese newspaper that the "time is ripe" for a loosening of the peg. The G7 meeting is thought unlikely to produce any meaningful movement in Chinese policy. In the meantime, the US Federal Reserve's decision on 2 February to boost interest rates by a quarter of a point - the sixth such move in as many months - has opened up a differential with European rates. The half-point window, some believe, could be enough to keep US assets looking more attractive, and could help prop up the dollar. The recent falls have partly been the result of big budget deficits, as well as the US's yawning current account gap, both of which need to be funded by the buying of US bonds and assets by foreign firms and governments. The White House will announce its budget on Monday, and many commentators believe the deficit will remain at close to half a trillion dollars.

"""

class Sentence:
    def __init__(self, text, start_offset, end_offset, ents):
        self.text = text
        self.start_offset = start_offset
        self.end_offset = end_offset
        self.person_entities = []
        self.org_entities = []
    
        self.process_entities(ents)

    def process_entities(self, entities):
        for entity in entities:
            if entity.label_ == "PERSON":
                self.person_entities.append(entity)
            elif entity.label_ == "ORG":
                self.org_entities.append(entity)

    def __repr__(self):
        return "<Sentence text: " + self.text[0:5] + " Per/Org: " + str(len(self.person_entities)) +"/" + str(len(self.org_entities)) + " start/end " + str(self.start_offset) + "/" + str(self.end_offset) + ">" 

class Document:
    def __init__(self):
        self.text = None
        self.processed = None
        self.spacy_object = None
        self.sentences = None

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def process(self):
        try:
            self.spacy_object = nlp(self.text)
            self.processed = True
            self.get_sentences()
        except:
            self.processed = False
    
    def get_sentences(self):
        self.sentences = [Sentence(sentence.text, sentence.start, sentence.end, sentence.ents) for sentence in self.spacy_object.sents]
        
    def get_relationship_candidates(self):
        candidates = [sentence for sentence in self.sentences if  len(sentence.org_entities) == 1]
        return candidates

if __name__ == "__main__":
    print("Starting a test")
    document = Document()
    print(document)
    document.set_text(sample)
    print(document.get_text())
    document.process()
    print("^" * 25)
    for sentence in document.get_relationship_candidates():
        print(sentence.text)
        print("\t", sentence.person_entities)
        print("\t", sentence.org_entities)
        print("$" * 25)
    