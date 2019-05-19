import logging.config
logger = logging.getLogger('counter')


import hashlib
import re
import gc

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

        row_text = re.sub(' +', ' ', row_text)
        row_text = re.sub('\n+', '\n', row_text)
        row_text = re.sub('\t+', '\t', row_text)
        row_text = re.sub('-+', '-', row_text)

        row_text.rstrip()
        row_text.lstrip()

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
        logger.debug("Simply splitting text of some length: " + str(length_for_splitting) + " with separators: " + str(separators))


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

        logger.debug("Total subelements of simple split: " + str(len(simple_split)))
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


class id_management():
    all_ids = {}

    def __init__(self):
        pass

    @staticmethod
    def calc_id(unified_text="", text=""):

        if unified_text != "":
            text_to_encode = unified_text[:]
            return hashlib.sha256(text_to_encode.encode()).hexdigest()
        else:
            text_to_encode = text_unification.unification(text)[:]
            return hashlib.sha256(text_to_encode.encode()).hexdigest()

    @classmethod
    def clear_all(cls):
        for some in cls.all_ids.values():
            del some

        cls.all_ids = {}
        gc.collect()

    @classmethod
    def get_by_id(cls, id=0):

        if id == 0:
            return cls.all_ids.keys()
        elif id in cls.all_ids.keys():
            return cls.all_ids.get(id)
        else:
            logger.warning("Requested id absent in all ids storage and != 0, id: " + str(id))
            return False

    @classmethod
    def get_all_ids(cls):
        logger.debug("Getting all entities IDs, total:" + str(len(cls.all_ids.values())) + " Class: " + str(cls.__name__))
        return cls.all_ids.keys()


    @classmethod
    def get_all(cls):
        logger.debug("Getting all entities obj, total:" + str(len(cls.all_ids.values())) + "Class: " + str(cls.__name__))
        return cls.all_ids.values()

    @classmethod
    def safe_create(cls,name):
        id=cls.calc_id(text=name)

        if id in cls.all_ids.keys():
            return cls.all_ids.get(id)
        else:
            return cls(name)

    def get_unified_text(self):
        return text_unification.unification(self.text)

    def set_db_sync(self,db_sync=True):
        self.__db_sync=db_sync



class word(id_management):
    #list all: text: word_obj
    #all={}

    all_ids={}
    #id - object_link

    def __init__(self, text):
        self.unified_text = text_unification.unification(text)
        self.id = word.calc_id(unified_text=self.unified_text)
        word.all_ids[self.id] = self

        self.type=""

        self.__subwords = {}
        # subword_id, cound

        self.decomposed_flag=False

        logger.debug("hash: \'"+ str(self.id) + "\' word " + self.unified_text + " created")

    def get_subwords(self):
        return self.__subwords.items()

    @staticmethod
    def get_ids_sorted_desc_by_subwords(word_ids=[]):

        sorting_word_ids=[]

        if len(word_ids)==0:
            sorting_word_ids=word.get_all_ids()
        else:
            sorting_word_ids=word_ids


        # sort all word_ids from 0 subbowrds to maximum and returns a list
        logger.info("Starting Sorting word_ids by subwords count descending")

        word_ids_with_sub_number = {}

        for word_id in sorting_word_ids:
            someword=word.get_by_id(word_id)
            word_ids_with_sub_number[word_id] = len(someword.get_subwords())

        sorted_word_ids_with_sub_number=sorted(word_ids_with_sub_number.items(), key=lambda x: x[1], reverse=True)
        # collected value - list of tuples

        sorted_word_ids=[]
        for i in range(len(sorted_word_ids_with_sub_number)):
            sorted_word_ids.append(sorted_word_ids_with_sub_number[i][0])


        logger.info("Sorting word_ids by subwords count descending - Finished")
        return sorted_word_ids

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

                    if someword.id not in self.__subwords.keys():
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


class author(id_management):
    all_ids = {}

    # id: object
    def __init__(self,name):
        self.name=str(name)
        self.id=author.calc_id(text=name)

        author.all_ids[self.id]=self


class source(id_management):
    all_ids={}
    #id: object

    def __init__(self,text):
        self.name=str(text)
        self.id=source.calc_id(text=text)

        source.all_ids[self.id] = self

class message(id_management):
    all_ids={}

    def __init__(self,text,language=""):
        self.unified_text=text_unification.unification(text)

        self.text=text

        self.id=message.calc_id(unified_text=self.unified_text)
        message.all_ids[self.id] = self

        self.date_creation = None
        self.language=""

        self.author_id=""
        self.source_id=""
        self.filename=""

        self.decomposed=False

        logger.debug("MSG " + str(self.id[0:6]) + "..." + self.id[-6:] + " created!)")
        logger.debug("All ids: " + str(message.all_ids))

    def decompose(self):
        text_word=word.safe_create(self.text)
        text_word.decompose()
        self.decomposed=True

        #for wordphrase in text_unification.splitting(text_word.unified_text,text_unification.all_words_separator):
        #    self.word_used_in_text(wordphrase)

    def __str__(self):
        return "Message " + str(self.id[0:6]) + "..." + self.id[-6:]


def clear_all():
    message.clear_all()
    author.clear_all()
    source.clear_all()
    word.clear_all()

