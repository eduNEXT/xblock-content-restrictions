
            (function(global){
                var ContentRestrictionsI18N = {
                  init: function() {
                    

'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});

  
  django.pluralidx = function(count) { return (count == 1) ? 0 : 1; };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  const newcatalog = {
    "Content With Access Restrictions": "Contenidos con restricciones de acceso",
    "Display Name": "Nombre a mostrar",
    "Incorrect Password Explanatory Message": "Mensaje explicativo de contrase\u00f1a incorrecta",
    "Incorrect password. Please try again.": "Contrase\u00f1a incorrecta. Por favor, int\u00e9ntelo de nuevo.",
    "Learners will need to type this password to access the content of the xblock. If the learner does not type the correct password, they will not have access to the content and will get an explanatory message instead. If the password is changed after the learner has already accessed the content, the learner will need to type the new password to access the content.": "Los estudiantes deber\u00e1n introducir esta contrase\u00f1a para acceder al contenido del xblock. Si el estudiante no introduce la contrase\u00f1a correcta, no tendr\u00e1 acceso al contenido y recibir\u00e1 un mensaje explicativo. Si la contrase\u00f1a se cambia despu\u00e9s de que el estudiante ya haya accedido al contenido, el estudiante tendr\u00e1 que escribir la nueva contrase\u00f1a para acceder al contenido.",
    "Password": "Contrase\u00f1a",
    "Password Explanatory Message": "Mensaje explicativo de la contrase\u00f1a",
    "Password Restriction": "Restricci\u00f3n de contrase\u00f1a",
    "Please enter the password to access this content.": "Introduzca la contrase\u00f1a para acceder a este contenido.",
    "Submit": "Enviar",
    "The display name for this component.": "El nombre para mostrar de este componente.",
    "This message will be shown when the learner enters an incorrect password.": "Este mensaje se mostrar\u00e1 cuando el estudiante introduzca una contrase\u00f1a incorrecta.",
    "This message will be shown when the learner is prompted to enter the password.": "Este mensaje se mostrar\u00e1 cuando se pida al estudiante que introduzca la contrase\u00f1a.",
    "When enabled, the content will be restricted by password.": "Si esta opci\u00f3n est\u00e1 activa, entonces el contenido estar\u00e1 restringido por contrase\u00f1a."
  };
  for (const key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      const value = django.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      const value = django.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      let value = django.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      let value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "j \\d\\e F \\d\\e Y \\a \\l\\a\\s H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d/%m/%Y %H:%M:%S",
      "%d/%m/%Y %H:%M:%S.%f",
      "%d/%m/%Y %H:%M",
      "%d/%m/%y %H:%M:%S",
      "%d/%m/%y %H:%M:%S.%f",
      "%d/%m/%y %H:%M",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j \\d\\e F \\d\\e Y",
    "DATE_INPUT_FORMATS": [
      "%d/%m/%Y",
      "%d/%m/%y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j \\d\\e F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "d/m/Y H:i",
    "SHORT_DATE_FORMAT": "d/m/Y",
    "THOUSAND_SEPARATOR": "\u00a0",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F \\d\\e Y"
  };

    django.get_format = function(format_type) {
      const value = django.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }
};


                  }
                };
                ContentRestrictionsI18N.init();
                global.ContentRestrictionsI18N = ContentRestrictionsI18N;
            }(this));
        