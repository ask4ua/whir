import logging.config

logger = logging.getLogger('counter')

class text_unification:
    # Only Textual Output


    #block_separators = ['\r','\t','\n']

    # [0] separator is used to add to the end of line for sure

    block_separators = ['\n','\t']
    sentense_separators = ['.','!','?','...'] + block_separators[0:1]
    phrase_separators = [',',':', ';','- ','"','\(','\)','\{','\}','\[','\]'] + sentense_separators[0:1]
    words_in_phrase_separators = [' '] + phrase_separators[0:1]

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

        ## In such case \n also hidden
        #row_text=' '.join(row_text.split())
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
        length_for_splitting=len(unified_text)
        logger.info("Simply splitting text of some length: " + str(length_for_splitting) + " with separators: " + str(separators))


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

        logger.info("Total subelements of simple split: " + str(len(simple_split)))
        return simple_split

        # now collected all cases
        # below also collecting it`s combinations

    def just_combine(simple_split,separators):
        logger.info("Combining text of such sublocks amount: " + str(len(simple_split)))

        subphrases_and_words=[]

        counter=0
        for firstword in range(len(simple_split)):
            for lastword in range(firstword + 1, len(simple_split) + 1):
            #for lastword in range(firstword, firstword + 2):
                if firstword == 0 and lastword == len(simple_split):
                    # case when the all phrase identified like a subphrase should be excluded
                    continue

                if firstword == lastword-1:
                    # case when the last word is recounted again like in simple split
                    continue

                subphrase = ""
                for wordphrase_combination in simple_split[firstword:lastword]:
                    subphrase += str(wordphrase_combination)
                    subphrase += separators[0]
                    pass

                subphrase = subphrase[0:-1]
                subphrases_and_words.append(subphrase)
                counter+=1
                logger.debug("Just Combine counter: " + str(counter))

        logger.info("Total combinations: " + str(len(subphrases_and_words)))

        return subphrases_and_words

    def full_splitting(unified_text, separators):


        simple_split = text_unification.just_split(unified_text, separators)
        subphrases_and_words = text_unification.just_combine(simple_split, separators)


        logger.debug(
            "For word " + str(unified_text) + " identified such subwords: " + str(simple_split + subphrases_and_words))

        return simple_split + subphrases_and_words

class word():
    #list all: text: word_obj
    #all={}

    __all_ids={}
    #id - object_link

    @staticmethod
    def id(text="",unified_text=""):

        if unified_text != "":
            return hash(text_unification.unification(unified_text))
        else:
            return hash(unified_text)

    def __init__(self,text):
        self.unified_text = text_unification.unification(text)
        self.id=word.id(unified_text=self.unified_text)

        self.type=""

        word.__all_ids[self.id]=self

        self.__subwords = {}
        # subword_id, cound

        self.decomposed_flag=False

        logger.debug("hash: \'"+ str(self.id) + "\' word " + self.unified_text + " created")

    def return_subwords(self):
        return self.__subwords.copy()

    def set_db_sync(self,db_sync=True):
        self.__db_sync=db_sync

    @staticmethod
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

        decomposing_level=0
        for separator in text_unification.separators:
            if text_unification.split_check(self.unified_text,separators=separator):

                if decomposing_level==0:
                    submessages=text_unification.just_split(self.unified_text,separator)
                    self.type='blok'

                elif decomposing_level==1:
                    submessages = text_unification.full_splitting(self.unified_text, separator)
                    self.type = 'sentense'

                elif decomposing_level==2:
                    submessages = text_unification.full_splitting(self.unified_text, separator)
                    self.type = 'phrase'

                elif decomposing_level==3:
                    submessages = text_unification.full_splitting(self.unified_text, separator)
                    self.type='word'

                else:
                    submessages = text_unification.full_splitting(self.unified_text, separator)
                    logger.warning("Text not identified as blok, sentense, phrase or word!")


                for submessage in submessages:

                    # if some text block already in db - no sence to decompose it for the 2-nd time!
                    someword = word.safe_create(submessage)

                    if someword.id not in self.__subwords:
                        self.__subwords[someword.id] = 1
                        logger.debug(str(someword.unified_text) + " counted first time inside " + str(self.unified_text))
                    else:
                        self.__subwords[someword.id] += 1
                        logger.debug(str(someword.unified_text) + " counted " + str(self.__subwords[someword.id]) + " time inside " + str(self.unified_text))

                    if not someword.decomposed_flag:
                        someword.decompose()
                    #msg.word_used_in_text(someword.unified_text)

                #logger.info("Finished decomposing of word of such lenght:" + str(len(self.unified_text)))
                break

                #add to msg self_id

        self.decomposed_flag = True
        decomposing_level +=1

        #logger.debug("subowrds for word " + str(self.unified_text) + " is " + str(self.__subwords))


    #subword is only linking to existing words
    #counting performed under message

    def getsubwords(self):
        return self.__subwords

    @staticmethod
    def print_all_words():
        for someword in word.__all_ids.values():
            print(someword.unified_text + " of type" + str(someword.type) + "reusing such words:" + str(len(someword.getsubwords())))
            #for subword_id,count in someword.getsubwords().items():
            #    subword=word.get_by_id(subword_id)
            #    print(" - " + str(subword.unified_text) + " used " + str(count) + " times")

class message():
    __all_messages=[]

    def __init__(self,text,language=""):
        self.__allwords = {}
        self.text=text

        # word_id : count usages
        message.__all_messages.append(self)

        self.date_creation = None
        self.language=""

        self.decomposed=False

    @staticmethod
    def get_all_messages():
        return message.__all_messages

    def word_used_in_text(self,unified_text):
        someword=word.safe_create(unified_text)

        if someword.id in self.__allwords.keys():
            self.__allwords[someword.id]+=1
        else:
            self.__allwords[someword.id]=1

        logger.debug("Word " + str(unified_text) + " registered as used in " + str(self.text))

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

        self.decomposed=True

        #for wordphrase in text_unification.splitting(text_word.unified_text,text_unification.all_words_separator):
        #    self.word_used_in_text(wordphrase)


