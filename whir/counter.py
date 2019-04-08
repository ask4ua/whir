import logging.config
logger = logging.getLogger('counter')


class text_unification:
    # Only Textual Output

    block_separators = ["\r",'\t','\n']
    phrase_separators = [':', ';', ',', '!', '?', '- ', '.']
    words_in_phrase_separators = [' ']

    def unification(row_text):
        #change multiple spaces by 1 space
        #trim spaces before comas, dots etc.


        text=row_text.strip()
        return text

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

        # Found Phrases - create words, add them to subwords
        # Found Words in Phrases, add them to subwords of Phrases and overall Subwords


        if text_unification.split_check(self.unified_text,text_unification.block_separators):
            for submessage_block in text_unification.splitting(self.unified_text,text_unification.block_separators):
                block=word.safe_create(submessage_block)
                block.decompose()

                if block.id not in self.__subwords:
                    self.__subwords[block.id] = 1
                    logger.debug(str(submessage_block) + " counted first time")
                else:
                    self.__subwords[block.id] += 1
                    logger.debug(str(submessage_block) + " counted " + str(self.__subwords[block.id]) + " time")

        elif text_unification.split_check(self.unified_text,text_unification.phrase_separators+text_unification.block_separators):
            for submessage_phrase in text_unification.splitting(self.unified_text,text_unification.phrase_separators):
                somephrase=word.safe_create(submessage_phrase)
                somephrase.decompose()

                if someword.id not in self.__subwords:
                    self.__subwords[somephrase.id] = 1
                    logger.debug(str(submessage_phrase) + " counted first time")
                else:
                    self.__subwords[somephrase.id] += 1
                    logger.debug(str(submessage_phrase) + " counted " + str(self.__subwords[somephrase.id]) + " time")


        elif text_unification.split_check(self.unified_text,text_unification.words_in_phrase_separators+text_unification.phrase_separators):

            for subphrase_word in text_unification.just_split(self.unified_text,text_unification.words_in_phrase_separators):
                someword=word.safe_create(text_unification.unification(subphrase_word))

                if someword.id not in self.__subwords:
                    self.__subwords[someword.id] = 1
                    logger.debug(str(subphrase_word) + " counted first time")
                else:
                    self.__subwords[someword.id] += 1
                    logger.debug(str(subphrase_word) + " counted " + str(self.__subwords[someword.id]) + " time")

        logger.debug("subowrds for word " + str(self.unified_text) + " is " + str(self.__subwords))

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

        if someword.id in self.__all_words.keys():
            self.__all_words[someword.id]+=1
        else:
            self.__all_words[someword.id]=1

    def print_all_words(self):
        logger.debug("Printing all messages")
        logger.debug(str(self.__allwords))

        for (word_id, count) in self.__allwords.items():
            print(word_id,'\''+str(word.get_by_id(word_id).unified_text)+'\''," counted",count,"times")

    def decompose(self):
        text_word=word.safe_create(self.text)
        self.__allwords =text_word.decompose()


