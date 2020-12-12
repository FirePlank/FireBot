import markdown
try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

def validate_language(language):
    # ISO 639-1 code validation
    # language source: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    codes = ["ab", "aa", "ae", "af", "ak", "am", "an", "ar", "as", "av", "ay",
             "az", "ba", "be", "bg", "bh", "bi", "bm", "bn", "bo", "br", "bs",
             "ca", "ce", "ch", "co", "cr", "cs", "cu", "cv", "cy", "da", "de",
             "dv", "dz", "ee", "el", "en", "eo", "es", "et", "eu", "fa", "ff",
             "fi", "fj", "fo", "fr", "fy", "ga", "gd", "gl", "gn", "gu", "gv",
             "ha", "he", "hi", "ho", "hr", "ht", "hu", "hy", "hz", "ia", "id",
             "ie", "ig", "ii", "ik", "io", "is", "it", "iu", "ja", "jv", "ka",
             "kg", "ki", "kj", "kk", "kl", "km", "kn", "ko", "kr", "ks", "ku",
             "kv", "kw", "ky", "la", "lb", "lg", "li", "ln", "lo", "lt", "lu",
             "lv", "mg", "mh", "mi", "mk", "ml", "mn", "mr", "ms", "mt", "my",
             "na", "nb", "nd", "ne", "ng", "nl", "nn", "no", "nr", "nv", "ny",
             "oc", "oj", "om", "or", "os", "pa", "pi", "ps", "pt", "qu", "rm",
             "rn", "ro", "ru", "rw", "sa", "sc", "sd", "se", "sg", "si", "sk",
             "sl", "sm", "sn", "so", "sq", "sr", "ss", "st", "su", "sv", "sw",
             "ta", "te", "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "ts",
             "tt", "tw", "ty", "ug", "uk", "ur", "uz", "ve", "vi", "vo", "wa",
             "wo", "xh", "yi", "yo", "za", "zh", "zu"]
    return language.lower() in codes


def remove_html(text, md=False):
    if md:
        text = markdown.markdown(text)
    # credit: stackoverflow
    class MLStripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self.reset()
            self.strict = False
            self.convert_charrefs= True
            self.fed = []
        def handle_data(self, d):
            self.fed.append(d)
        def get_data(self):
            return ''.join(self.fed)

    s = MLStripper()
    s.feed(text)
    return s.get_data()