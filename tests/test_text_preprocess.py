from nirtools.text import preprocess


def test_get_lang_reserved_words():
    words = preprocess.get_lang_reserved_words("ruby")
    assert words == [
        "__ENCODING__", "__LINE__", "__FILE__", "BEGIN", "END", "alias", "and", "begin",
        "break", "case", "class", "def", "defined", "do", "else", "elsif", "end", "ensure",
        "false", "for", "if", "in", "module", "next", "nil", "not", "or", "redo", "rescue",
        "retry", "return", "self", "super", "then", "true", "undef", "unless", "until",
        "when", "while", "yield"]


def test_code_tokenize():
    code = "func ( t * SecondaryTree ) SeekFirst ( ) ( e * SecondaryEnumerator , err error ) { q := t . first if q == nil { return nil , io . EOF } return btEPool2 . get ( nil , true , 0 , q . d [ 0 ] . k , q , t , atomic . LoadUint64 ( & t . ver ) ) , nil }"
    expected = "func ( t * secondary tree ) seek first ( ) ( e * secondary enumerator , err error ) { q := t . " \
               "first if q == nil { return nil , io . eOF} return bt e pool2 . get ( nil , true , 0 , q . d [ 0 ] . " \
               "k , q , t , atomic . load uint64 ( & t . ver ) ) , nil }"
    assert preprocess.code_tokenize(code) == expected


def test_remove_non_alphabet():
    code = "func ( t * SecondaryTree ) SeekFirst ( ) ( e * SecondaryEnumerator , err error ) { q := t . first if q == nil { return nil , io . EOF } return btEPool2 . get ( nil , true , 0 , q . d [ 0 ] . k , q , t , atomic . LoadUint64 ( & t . ver ) ) , nil }"
    expected = "func t SecondaryTree SeekFirst e SecondaryEnumerator err error q t first if q nil return nil io EOF " \
               "return btEPool2 get nil true 0 q d 0 k q t atomic LoadUint64 t ver nil"
    assert preprocess.remove_non_alphabet(code) == expected


def test_remove_unicharacter():
    code = "func ( t * SecondaryTree ) SeekFirst ( ) ( e * SecondaryEnumerator , err error ) { q := t . first if q == nil { return nil , io . EOF } return btEPool2 . get ( nil , true , 0 , q . d [ 0 ] . k , q , t , atomic . LoadUint64 ( & t . ver ) ) , nil }"
    expected = "func SecondaryTree SeekFirst SecondaryEnumerator err error q := t first if q == nil return nil io " \
               "EOF return btEPool2 get nil true atomic LoadUint64 ver nil"
    assert preprocess.remove_unicharacter(code) == expected

