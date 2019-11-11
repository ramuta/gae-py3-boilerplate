import logging
from importlib import import_module


def get_translation(locale, translation_function):
    translation = None

    try:
        translations = import_module("translations.{}".format(locale))
        translation = getattr(translations, translation_function)()
    except ImportError as e:
        logging.warning(e)
    except AttributeError as e:
        logging.warning("{} {}. Will try the English translation instead.".format(locale, e))

    if not translation:
        try:
            translations = import_module("translations.en")
            translation = getattr(translations, translation_function)()
        except AttributeError as e:
            logging.warning("en {}".format(e))

    return translation
