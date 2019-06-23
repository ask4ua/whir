Text="""Multiline, prechecked - but will all symbols, text like: " symbol, ' symbol, % symbol, and 2% symbol.
    Why is it written? To proceed with 'unit tests'!)
    Check and Count for sure.
    
    P.S.: and blah, blah, blah."""

Decomposition = \
{'multiline, prechecked ,but will all symbols, text like, , symbol, , symbol, % symbol, and 2% symbol.\n why is it written. to proceed with ,unit tests,.,\n check and count for sure.\n \n p.s., and blah, blah, blah':
  {'multiline, prechecked ,but will all symbols, text like, , symbol, , symbol, % symbol, and 2% symbol': 1,
   'why is it written. to proceed with ,unit tests,.': 1,
   'check and count for sure': 1,
   '': 1, 'p.s., and blah, blah, blah': 1},
 'multiline, prechecked ,but will all symbols, text like, , symbol, , symbol, % symbol, and 2% symbol':
  {'multiline': 1,
   'prechecked': 1,
   'but will all symbols': 1,
   'text like': 1, '': 2,
   'symbol': 2, '% symbol': 1,
   'and 2% symbol': 1, 'multiline, prechecked': 1, 'multiline, prechecked ,but will all symbols': 1, 'multiline, prechecked ,but will all symbols, text like': 1, 'multiline, prechecked ,but will all symbols, text like,': 1, 'multiline, prechecked ,but will all symbols, text like, , symbol': 1, 'multiline, prechecked ,but will all symbols, text like, , symbol,': 1, 'multiline, prechecked ,but will all symbols, text like, , symbol, , symbol': 1, 'multiline, prechecked ,but will all symbols, text like, , symbol, , symbol, % symbol': 1, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'prechecked ,but will all symbols, text like,': 1, 'prechecked ,but will all symbols, text like, , symbol': 1, 'prechecked ,but will all symbols, text like, , symbol,': 1, 'prechecked ,but will all symbols, text like, , symbol, , symbol': 1, 'prechecked ,but will all symbols, text like, , symbol, , symbol, % symbol': 1, 'prechecked ,but will all symbols, text like, , symbol, , symbol, % symbol, and 2% symbol': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'but will all symbols, text like, , symbol,': 1, 'but will all symbols, text like, , symbol, , symbol': 1, 'but will all symbols, text like, , symbol, , symbol, % symbol': 1, 'but will all symbols, text like, , symbol, , symbol, % symbol, and 2% symbol': 1, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, 'text like, , symbol, , symbol': 1, 'text like, , symbol, , symbol, % symbol': 1, 'text like, , symbol, , symbol, % symbol, and 2% symbol': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, ', symbol, , symbol, % symbol': 1, ', symbol, , symbol, % symbol, and 2% symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, 'symbol, , symbol, % symbol': 1, 'symbol, , symbol, % symbol, and 2% symbol': 1, ', symbol, % symbol': 1, ', symbol, % symbol, and 2% symbol': 1, 'symbol, % symbol': 1, 'symbol, % symbol, and 2% symbol': 1, '% symbol, and 2% symbol': 1}, 'multiline': {}, 'prechecked': {}, 'but will all symbols': {'but': 1, 'will': 1, 'all': 1, 'symbols': 1, 'but will': 1, 'but will all': 1, 'will all': 1, 'will all symbols': 1, 'all symbols': 1}, 'but': {}, 'will': {}, 'all': {}, 'symbols': {}, 'but will': {'but': 1, 'will': 1}, 'but will all': {'but': 1, 'will': 1, 'all': 1, 'but will': 1, 'will all': 1}, 'will all': {'will': 1, 'all': 1}, 'will all symbols': {'will': 1, 'all': 1, 'symbols': 1, 'will all': 1, 'all symbols': 1}, 'all symbols': {'all': 1, 'symbols': 1}, 'text like': {'text': 1, 'like': 1}, 'text': {}, 'like': {}, '': {}, 'symbol': {}, '% symbol': {'%': 1, 'symbol': 1}, '%': {}, 'and 2% symbol': {'and': 1, '2%': 1, 'symbol': 1, 'and 2%': 1, '2% symbol': 1}, 'and': {}, '2%': {}, 'and 2%': {'and': 1, '2%': 1}, '2% symbol': {'2%': 1, 'symbol': 1}, 'multiline, prechecked': {'multiline': 1, 'prechecked': 1}, 'multiline, prechecked ,but will all symbols': {'multiline': 1, 'prechecked': 1, 'but will all symbols': 1, 'multiline, prechecked': 1, 'prechecked ,but will all symbols': 1}, 'prechecked ,but will all symbols': {'prechecked': 1, 'but will all symbols': 1}, 'multiline, prechecked ,but will all symbols, text like': {'multiline': 1, 'prechecked': 1, 'but will all symbols': 1, 'text like': 1, 'multiline, prechecked': 1, 'multiline, prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'but will all symbols, text like': 1}, 'prechecked ,but will all symbols, text like': {'prechecked': 1, 'but will all symbols': 1, 'text like': 1, 'prechecked ,but will all symbols': 1, 'but will all symbols, text like': 1}, 'but will all symbols, text like': {'but will all symbols': 1, 'text like': 1}, 'multiline, prechecked ,but will all symbols, text like,': {'multiline': 1, 'prechecked': 1, 'but will all symbols': 1, 'text like': 1, 'multiline, prechecked': 1, 'multiline, prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'but will all symbols, text like': 1}, 'multiline, prechecked ,but will all symbols, text like, , symbol': {'multiline': 1, 'prechecked': 1, 'but will all symbols': 1, 'text like': 1, '': 1, 'symbol': 1, 'multiline, prechecked': 1, 'multiline, prechecked ,but will all symbols': 1, 'multiline, prechecked ,but will all symbols, text like': 1, 'multiline, prechecked ,but will all symbols, text like,': 1, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'prechecked ,but will all symbols, text like,': 1, 'prechecked ,but will all symbols, text like, , symbol': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'text like,': 1, 'text like, , symbol': 1, ', symbol': 1}, 'prechecked ,but will all symbols, text like,': {'prechecked': 1, 'but will all symbols': 1, 'text like': 1, 'prechecked ,but will all symbols': 1, 'but will all symbols, text like': 1}, 'prechecked ,but will all symbols, text like, , symbol': {'prechecked': 1, 'but will all symbols': 1, 'text like': 1, '': 1, 'symbol': 1, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'prechecked ,but will all symbols, text like,': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'text like,': 1, 'text like, , symbol': 1, ', symbol': 1}, 'but will all symbols, text like,': {'but will all symbols': 1, 'text like': 1}, 'but will all symbols, text like, , symbol': {'but will all symbols': 1, 'text like': 1, '': 1, 'symbol': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'text like,': 1, 'text like, , symbol': 1, ', symbol': 1}, 'text like,': {'text': 1, 'like': 1}, 'text like, , symbol': {'text like': 1, '': 1, 'symbol': 1, 'text like,': 1, ', symbol': 1}, ', symbol': {'': 1, 'symbol': 1}, 'multiline, prechecked ,but will all symbols, text like, , symbol,': {'multiline': 1, 'prechecked': 1, 'but will all symbols': 1, 'text like': 1, '': 1, 'symbol': 1, 'multiline, prechecked': 1, 'multiline, prechecked ,but will all symbols': 1, 'multiline, prechecked ,but will all symbols, text like': 1, 'multiline, prechecked ,but will all symbols, text like,': 1, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'prechecked ,but will all symbols, text like,': 1, 'prechecked ,but will all symbols, text like, , symbol': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'text like,': 1, 'text like, , symbol': 1, ', symbol': 1}, 'multiline, prechecked ,but will all symbols, text like, , symbol, , symbol': {'multiline': 1, 'prechecked': 1, 'but will all symbols': 1, 'text like': 1, '': 2, 'symbol': 2, 'multiline, prechecked': 1, 'multiline, prechecked ,but will all symbols': 1, 'multiline, prechecked ,but will all symbols, text like': 1, 'multiline, prechecked ,but will all symbols, text like,': 1, 'multiline, prechecked ,but will all symbols, text like, , symbol': 1, 'multiline, prechecked ,but will all symbols, text like, , symbol,': 1, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'prechecked ,but will all symbols, text like,': 1, 'prechecked ,but will all symbols, text like, , symbol': 1, 'prechecked ,but will all symbols, text like, , symbol,': 1, 'prechecked ,but will all symbols, text like, , symbol, , symbol': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'but will all symbols, text like, , symbol,': 1, 'but will all symbols, text like, , symbol, , symbol': 1, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, 'text like, , symbol, , symbol': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1}, 'prechecked ,but will all symbols, text like, , symbol,': {'prechecked': 1, 'but will all symbols': 1, 'text like': 1, '': 1, 'symbol': 1, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'prechecked ,but will all symbols, text like,': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'text like,': 1, 'text like, , symbol': 1, ', symbol': 1}, 'prechecked ,but will all symbols, text like, , symbol, , symbol': {'prechecked': 1, 'but will all symbols': 1, 'text like': 1, '': 2, 'symbol': 2, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'prechecked ,but will all symbols, text like,': 1, 'prechecked ,but will all symbols, text like, , symbol': 1, 'prechecked ,but will all symbols, text like, , symbol,': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'but will all symbols, text like, , symbol,': 1, 'but will all symbols, text like, , symbol, , symbol': 1, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, 'text like, , symbol, , symbol': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1}, 'but will all symbols, text like, , symbol,': {'but will all symbols': 1, 'text like': 1, '': 1, 'symbol': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'text like,': 1, 'text like, , symbol': 1, ', symbol': 1}, 'but will all symbols, text like, , symbol, , symbol': {'but will all symbols': 1, 'text like': 1, '': 2, 'symbol': 2, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'but will all symbols, text like, , symbol,': 1, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, 'text like, , symbol, , symbol': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1}, 'text like, , symbol,': {'text like': 1, '': 1, 'symbol': 1, 'text like,': 1, ', symbol': 1}, 'text like, , symbol, , symbol': {'text like': 1, '': 2, 'symbol': 2, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1}, ', symbol,': {'': 1, 'symbol': 1}, ', symbol, , symbol': {'symbol': 2, '': 1, 'symbol,': 1, ', symbol': 1}, 'symbol,': {}, 'symbol, , symbol': {'symbol': 2, '': 1, 'symbol,': 1, ', symbol': 1}, 'multiline, prechecked ,but will all symbols, text like, , symbol, , symbol, % symbol': {'multiline': 1, 'prechecked': 1, 'but will all symbols': 1, 'text like': 1, '': 2, 'symbol': 2, '% symbol': 1, 'multiline, prechecked': 1, 'multiline, prechecked ,but will all symbols': 1, 'multiline, prechecked ,but will all symbols, text like': 1, 'multiline, prechecked ,but will all symbols, text like,': 1, 'multiline, prechecked ,but will all symbols, text like, , symbol': 1, 'multiline, prechecked ,but will all symbols, text like, , symbol,': 1, 'multiline, prechecked ,but will all symbols, text like, , symbol, , symbol': 1, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'prechecked ,but will all symbols, text like,': 1, 'prechecked ,but will all symbols, text like, , symbol': 1, 'prechecked ,but will all symbols, text like, , symbol,': 1, 'prechecked ,but will all symbols, text like, , symbol, , symbol': 1, 'prechecked ,but will all symbols, text like, , symbol, , symbol, % symbol': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'but will all symbols, text like, , symbol,': 1, 'but will all symbols, text like, , symbol, , symbol': 1, 'but will all symbols, text like, , symbol, , symbol, % symbol': 1, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, 'text like, , symbol, , symbol': 1, 'text like, , symbol, , symbol, % symbol': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, ', symbol, , symbol, % symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, 'symbol, , symbol, % symbol': 1, ', symbol, % symbol': 1, 'symbol, % symbol': 1}, 'prechecked ,but will all symbols, text like, , symbol, , symbol, % symbol': {'prechecked': 1, 'but will all symbols': 1, 'text like': 1, '': 2, 'symbol': 2, '% symbol': 1, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'prechecked ,but will all symbols, text like,': 1, 'prechecked ,but will all symbols, text like, , symbol': 1, 'prechecked ,but will all symbols, text like, , symbol,': 1, 'prechecked ,but will all symbols, text like, , symbol, , symbol': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'but will all symbols, text like, , symbol,': 1, 'but will all symbols, text like, , symbol, , symbol': 1, 'but will all symbols, text like, , symbol, , symbol, % symbol': 1, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, 'text like, , symbol, , symbol': 1, 'text like, , symbol, , symbol, % symbol': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, ', symbol, , symbol, % symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, 'symbol, , symbol, % symbol': 1, ', symbol, % symbol': 1, 'symbol, % symbol': 1}, 'but will all symbols, text like, , symbol, , symbol, % symbol': {'but will all symbols': 1, 'text like': 1, '': 2, 'symbol': 2, '% symbol': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'but will all symbols, text like, , symbol,': 1, 'but will all symbols, text like, , symbol, , symbol': 1, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, 'text like, , symbol, , symbol': 1, 'text like, , symbol, , symbol, % symbol': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, ', symbol, , symbol, % symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, 'symbol, , symbol, % symbol': 1, ', symbol, % symbol': 1, 'symbol, % symbol': 1}, 'text like, , symbol, , symbol, % symbol': {'text like': 1, '': 2, 'symbol': 2, '% symbol': 1, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, 'text like, , symbol, , symbol': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, ', symbol, , symbol, % symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, 'symbol, , symbol, % symbol': 1, ', symbol, % symbol': 1, 'symbol, % symbol': 1}, ', symbol, , symbol, % symbol': {'symbol': 2, '': 1, '% symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, ', symbol': 1, ', symbol, % symbol': 1, 'symbol, % symbol': 1}, ', symbol, % symbol': {'symbol': 1, '% symbol': 1}, 'symbol, % symbol': {'symbol': 1, '% symbol': 1}, 'symbol, , symbol, % symbol': {'symbol': 2, '': 1, '% symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, ', symbol': 1, ', symbol, % symbol': 1, 'symbol, % symbol': 1}, 'prechecked ,but will all symbols, text like, , symbol, , symbol, % symbol, and 2% symbol': {'prechecked': 1, 'but will all symbols': 1, 'text like': 1, '': 2, 'symbol': 2, '% symbol': 1, 'and 2% symbol': 1, 'prechecked ,but will all symbols': 1, 'prechecked ,but will all symbols, text like': 1, 'prechecked ,but will all symbols, text like,': 1, 'prechecked ,but will all symbols, text like, , symbol': 1, 'prechecked ,but will all symbols, text like, , symbol,': 1, 'prechecked ,but will all symbols, text like, , symbol, , symbol': 1, 'prechecked ,but will all symbols, text like, , symbol, , symbol, % symbol': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'but will all symbols, text like, , symbol,': 1, 'but will all symbols, text like, , symbol, , symbol': 1, 'but will all symbols, text like, , symbol, , symbol, % symbol': 1, 'but will all symbols, text like, , symbol, , symbol, % symbol, and 2% symbol': 1, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, 'text like, , symbol, , symbol': 1, 'text like, , symbol, , symbol, % symbol': 1, 'text like, , symbol, , symbol, % symbol, and 2% symbol': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, ', symbol, , symbol, % symbol': 1, ', symbol, , symbol, % symbol, and 2% symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, 'symbol, , symbol, % symbol': 1, 'symbol, , symbol, % symbol, and 2% symbol': 1, ', symbol, % symbol': 1, ', symbol, % symbol, and 2% symbol': 1, 'symbol, % symbol': 1, 'symbol, % symbol, and 2% symbol': 1, '% symbol, and 2% symbol': 1}, 'but will all symbols, text like, , symbol, , symbol, % symbol, and 2% symbol': {'but will all symbols': 1, 'text like': 1, '': 2, 'symbol': 2, '% symbol': 1, 'and 2% symbol': 1, 'but will all symbols, text like': 1, 'but will all symbols, text like,': 1, 'but will all symbols, text like, , symbol': 1, 'but will all symbols, text like, , symbol,': 1, 'but will all symbols, text like, , symbol, , symbol': 1, 'but will all symbols, text like, , symbol, , symbol, % symbol': 1, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, 'text like, , symbol, , symbol': 1, 'text like, , symbol, , symbol, % symbol': 1, 'text like, , symbol, , symbol, % symbol, and 2% symbol': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, ', symbol, , symbol, % symbol': 1, ', symbol, , symbol, % symbol, and 2% symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, 'symbol, , symbol, % symbol': 1, 'symbol, , symbol, % symbol, and 2% symbol': 1, ', symbol, % symbol': 1, ', symbol, % symbol, and 2% symbol': 1, 'symbol, % symbol': 1, 'symbol, % symbol, and 2% symbol': 1, '% symbol, and 2% symbol': 1}, 'text like, , symbol, , symbol, % symbol, and 2% symbol': {'text like': 1, '': 2, 'symbol': 2, '% symbol': 1, 'and 2% symbol': 1, 'text like,': 1, 'text like, , symbol': 1, 'text like, , symbol,': 1, 'text like, , symbol, , symbol': 1, 'text like, , symbol, , symbol, % symbol': 1, ', symbol': 2, ', symbol,': 1, ', symbol, , symbol': 1, ', symbol, , symbol, % symbol': 1, ', symbol, , symbol, % symbol, and 2% symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, 'symbol, , symbol, % symbol': 1, 'symbol, , symbol, % symbol, and 2% symbol': 1, ', symbol, % symbol': 1, ', symbol, % symbol, and 2% symbol': 1, 'symbol, % symbol': 1, 'symbol, % symbol, and 2% symbol': 1, '% symbol, and 2% symbol': 1}, ', symbol, , symbol, % symbol, and 2% symbol': {'symbol': 2, '': 1, '% symbol': 1, 'and 2% symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, 'symbol, , symbol, % symbol': 1, ', symbol': 1, ', symbol, % symbol': 1, ', symbol, % symbol, and 2% symbol': 1, 'symbol, % symbol': 1, 'symbol, % symbol, and 2% symbol': 1, '% symbol, and 2% symbol': 1}, ', symbol, % symbol, and 2% symbol': {'symbol': 1, '% symbol': 1, 'and 2% symbol': 1, 'symbol, % symbol': 1, '% symbol, and 2% symbol': 1}, '% symbol, and 2% symbol': {'% symbol': 1, 'and 2% symbol': 1}, 'symbol, % symbol, and 2% symbol': {'symbol': 1, '% symbol': 1, 'and 2% symbol': 1, 'symbol, % symbol': 1, '% symbol, and 2% symbol': 1}, 'symbol, , symbol, % symbol, and 2% symbol': {'symbol': 2, '': 1, '% symbol': 1, 'and 2% symbol': 1, 'symbol,': 1, 'symbol, , symbol': 1, 'symbol, , symbol, % symbol': 1, ', symbol': 1, ', symbol, % symbol': 1, ', symbol, % symbol, and 2% symbol': 1, 'symbol, % symbol': 1, 'symbol, % symbol, and 2% symbol': 1, '% symbol, and 2% symbol': 1}, 'why is it written. to proceed with ,unit tests,.': {'why is it written': 1, 'to proceed with ,unit tests': 1}, 'why is it written': {'why': 1, 'is': 1, 'it': 1, 'written': 1, 'why is': 1, 'why is it': 1, 'is it': 1, 'is it written': 1, 'it written': 1}, 'why': {}, 'is': {}, 'it': {}, 'written': {}, 'why is': {'why': 1, 'is': 1}, 'why is it': {'why': 1, 'is': 1, 'it': 1, 'why is': 1, 'is it': 1}, 'is it': {'is': 1, 'it': 1}, 'is it written': {'is': 1, 'it': 1, 'written': 1, 'is it': 1, 'it written': 1}, 'it written': {'it': 1, 'written': 1}, 'to proceed with ,unit tests': {'to proceed with': 1, 'unit tests': 1}, 'to proceed with': {'to': 1, 'proceed': 1, 'with': 1, 'to proceed': 1, 'proceed with': 1}, 'to': {}, 'proceed': {}, 'with': {}, 'to proceed': {'to': 1, 'proceed': 1}, 'proceed with': {'proceed': 1, 'with': 1}, 'unit tests': {'unit': 1, 'tests': 1}, 'unit': {}, 'tests': {}, 'check and count for sure': {'check': 1, 'and': 1, 'count': 1, 'for': 1, 'sure': 1, 'check and': 1, 'check and count': 1, 'check and count for': 1, 'and count': 1, 'and count for': 1, 'and count for sure': 1, 'count for': 1, 'count for sure': 1, 'for sure': 1}, 'check': {}, 'count': {}, 'for': {}, 'sure': {}, 'check and': {'check': 1, 'and': 1}, 'check and count': {'check': 1, 'and': 1, 'count': 1, 'check and': 1, 'and count': 1}, 'and count': {'and': 1, 'count': 1}, 'check and count for': {'check': 1, 'and': 1, 'count': 1, 'for': 1, 'check and': 1, 'check and count': 1, 'and count': 1, 'and count for': 1, 'count for': 1}, 'and count for': {'and': 1, 'count': 1, 'for': 1, 'and count': 1, 'count for': 1}, 'count for': {'count': 1, 'for': 1}, 'and count for sure': {'and': 1, 'count': 1, 'for': 1, 'sure': 1, 'and count': 1, 'and count for': 1, 'count for': 1, 'count for sure': 1, 'for sure': 1}, 'count for sure': {'count': 1, 'for': 1, 'sure': 1, 'count for': 1, 'for sure': 1}, 'for sure': {'for': 1, 'sure': 1}, 'p.s., and blah, blah, blah': {'p': 1, 's': 1, 'and blah, blah, blah': 1}, 'p': {}, 's': {}, 'and blah, blah, blah': {'and blah': 1, 'blah': 2, 'and blah, blah': 1, 'blah, blah': 1}, 'and blah': {'and': 1, 'blah': 1}, 'blah': {}, 'and blah, blah': {'and blah': 1, 'blah': 1}, 'blah, blah': {'blah': 2}}