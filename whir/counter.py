import logging.config
logger = logging.getLogger('counter')

class text_unification:
    # Only Textual Output

    #block_separators = ['\r','\t','\n']
    block_separators = ['\n','\t','стаття','розділ']
    sentense_separators = ['.','!','?']
    phrase_separators = [':', ';', ',', '!', '?', '- ']
    words_in_phrase_separators = [' ']

    separators=[block_separators,sentense_separators,phrase_separators,words_in_phrase_separators]

    all_words_separator=[]
    for separator in separators:
        all_words_separator+=separator

    def unification(row_text):
        #change multiple spaces by 1 space
        #trim spaces before comas, dots etc.

        #multicharacters=[' ','\n','\t']
        #for character in multicharacters:
        #    row_text=character.join(row_text.split(character))

        row_text=' '.join(row_text.split())
        row_text=row_text.lower()

        return row_text

    def split_check(unified_text, separators=[' ']):
        # check is pslitting required
        count = 1
        for separator in separators:
            if len(unified_text.split(separator)) > count:
                logger.debug("deeper decompose is required for word: " + str(unified_text))
                return True

        return False

    def just_split(unified_text,separators):
        logger.debug("Splitting text of some length: " + str(len(unified_text)) + " separators: " + str(separators))

        simple_split = []
        simple_split.append(unified_text)

        for separator in separators:
            splitted_text_list = []
            for some_text in simple_split:
                for some_splitted_text in str(some_text).split(separator):

                    text=text_unification.unification(some_splitted_text)
                    if text != "":
                        splitted_text_list.append(text)

            simple_split = splitted_text_list.copy();

        return simple_split

        # now collected all cases
        # below also collecting it`s combinations

    def just_combine(simple_split):
        subphrases_and_words=[]
        for firstword in range(len(simple_split)):
            for lastword in range(firstword + 1, len(simple_split) + 1):
                if firstword == 0 and lastword == len(simple_split):
                    # case when the all phrase identified like a subphrase should be excluded
                    continue

                if firstword == lastword-1:
                    # case when the last word is recounted again like in simple split
                    continue

                subphrase = ""
                for wordphrase_combination in simple_split[firstword:lastword]:
                    subphrase += str(wordphrase_combination)
                    subphrase += " "
                subphrase = subphrase[0:-1]
                subphrases_and_words.append(subphrase)

        return subphrases_and_words

    def splitting(unified_text,separators):

        simple_split=text_unification.just_split(unified_text,separators)
        subphrases_and_words = text_unification.just_combine(simple_split)

        logger.debug("For word " + str(unified_text) + " identified such subwords: " + str(simple_split+subphrases_and_words))

        return simple_split+subphrases_and_words

class word():
    #list all: text: word_obj
    #all={}

    __all_ids={}
    #id - object_link

    def __init__(self,text):
        self.unified_text = text_unification.unification(text)
        self.id=hash(self.unified_text)

        word.__all_ids[self.id]=self

        self.__subwords = {}

        logger.debug("hash: \'"+ str(self.id) + "\' word " + self.unified_text + " created")

    def return_subwords(self):
        return self.__subwords.copy()

    def set_db_sync(self,db_sync=True):
        self.__db_sync=db_sync

    def safe_create(text):
        id=hash(text_unification.unification(text))

        if id in word.__all_ids.keys():
            entity = word.__all_ids[id]
        else:
            entity = word(text)

        return entity

    def get_by_id(id):
        if id in word.__all_ids.keys():
            return word.__all_ids[id]
        else:
            return False

    def decompose(self):
        self.__subwords = {}
        # word_ids, count

        for separator in text_unification.separators:
            if text_unification.split_check(self.unified_text, separator):
                for submessage in text_unification.splitting(self.unified_text,separator):
                    someword = word.safe_create(submessage)

                    if someword.id not in self.__subwords:
                        self.__subwords[someword.id] = 1
                        logger.debug(str(someword.unified_text) + " counted first time")
                    else:
                        self.__subwords[someword.id] += 1
                        logger.debug(str(someword.unified_text) + " counted " + str(self.__subwords[someword.id]) + " time")

                    someword.decompose()
                    #msg.word_used_in_text(someword.unified_text)

                break

                #add to msg self_id

        #logger.debug("subowrds for word " + str(self.unified_text) + " is " + str(self.__subwords))

        return self.__subwords.copy()


    #subword is only linking to existing words
    #counting performed under message


class message():
    def __init__(self,text,language=""):
        self.__allwords = {}
        self.text=text

        # word_id : count usages

        self.date_creation = None
        self.language=""

        self.decomposed=False

    def word_used_in_text(self,unified_text):
        someword=word.safe_create(unified_text)

        if someword.id in self.__allwords.keys():
            self.__allwords[someword.id]+=1
        else:
            self.__allwords[someword.id]=1

        logger.debug("Word " + str(unified_text) + " is used in " + str(self.text))
        logger.debug("all messages:  " + str(self.__allwords))

    def print_all_words(self):
        logger.debug("Printing all messages")
        logger.debug(str(self.__allwords))

        for (word_id, count) in self.__allwords.items():
            print(word_id,'\''+str(word.get_by_id(word_id).unified_text)+'\''," counted",count,"times")

    def get_unified_text(self):
        return text_unification.unification(self.text)

    def decompose(self):
        text_word=word.safe_create(self.text)
        text_word.decompose()

        for wordphrase in text_unification.splitting(text_word.unified_text,text_unification.all_words_separator):
            self.word_used_in_text(wordphrase)


