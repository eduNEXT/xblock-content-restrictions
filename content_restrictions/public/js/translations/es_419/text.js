
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
    "IP Restriction": "Restricci\u00f3n de IP",
    "IP Restriction Explanatory Message": "Mensaje explicativo de restricci\u00f3n por IP",
    "IP Whitelist": "Lista blanca de IP",
    "Incorrect Password Explanatory Message": "Mensaje explicativo de contrase\u00f1a incorrecta",
    "Incorrect password. Please try again.": "Contrase\u00f1a incorrecta. Por favor, int\u00e9ntelo de nuevo.",
    "Learners will need to type this password to access the content of the xblock. If the learner does not type the correct password, they will not have access to the content and will get an explanatory message instead. If the password is changed after the learner has already accessed the content, the learner will need to type the new password to access the content.": "Los estudiantes deber\u00e1n introducir esta contrase\u00f1a para acceder al contenido del xblock. Si el estudiante no introduce la contrase\u00f1a correcta, no tendr\u00e1 acceso al contenido y recibir\u00e1 un mensaje explicativo. Si la contrase\u00f1a se cambia despu\u00e9s de que el estudiante ya haya accedido al contenido, el estudiante tendr\u00e1 que escribir la nueva contrase\u00f1a para acceder al contenido.",
    "List of IP addresses or IP address ranges from which the content can be accessed. The compatible protocols are IPv4 and IPv6. If the learner's IP address is not in the whitelist, they will not have access to the content. The range should be in the CIDR format, e.g. (IPv4) \"192.168.1.0/24\", in this case only IP addresses from  \"192.168.1.0\" to \"192.168.1.255\" can access to the content, or (IPv6) \"2001:db8:85a3::/48\", in this case only IP addresses from \"2001:db8:85a3::\" to \"2001:db8:85a3:ffff:ffff:ffff:ffff:ffff\" can access to the content. Also, a single IP address can be provided, e.g. (IPv4) \"172.16.0.0\", or (IPv6) \"7ac:264a:dd69::\". Alternatively, is possible mix IP addresses and IP ranges with different formats, e.g. [\"192.168.1.0/24\", \"172.16.0.0\", \"65c1:e700::/24\", \"5c87::\"]": "Lista de direcciones IP o rangos de direcciones IP desde los cuales se puede acceder al contenido. Los protocolos compatibles son IPv4 e IPv6. Si la direcci\u00f3n IP del estudiante no est\u00e1 en la lista blanca, no tendr\u00e1 acceso al contenido. El rango debe estar en formato CIDR, por ejemplo (IPv4) \"192.168.1.0/24\", en este caso solo las direcciones IP desde \"192.168.1.0\" hasta \"192.168.1.255\" pueden acceder al contenido, o (IPv6) \"2001:db8:85a3::/48\", en este caso solo las direcciones IP desde \"2001:db8:85a3::\" hasta \"2001:db8:85a3:ffff:ffff:ffff:ffff:ffff\" pueden acceder al contenido. Tambi\u00e9n se puede proporcionar una sola direcci\u00f3n IP, por ejemplo (IPv4) \"172.16.0.0\", o (IPv6) \"7ac:264a:dd69::\". Alternativamente, es posible mezclar direcciones IP y rangos de direcciones IP con diferentes formatos, por ejemplo [\"192.168.1.0/24\", \"172.16.0.0\", \"65c1:e700::/24\", \"5c87::\"]",
    "Password": "Contrase\u00f1a",
    "Password Explanatory Message": "Mensaje explicativo de la contrase\u00f1a",
    "Password Restriction": "Restricci\u00f3n de contrase\u00f1a",
    "Please enter the password to access this content.": "Introduzca la contrase\u00f1a para acceder a este contenido.",
    "Submit": "Enviar",
    "The display name for this component.": "El nombre para mostrar de este componente.",
    "This message will be shown when the learner enters an incorrect password.": "Este mensaje se mostrar\u00e1 cuando el estudiante introduzca una contrase\u00f1a incorrecta.",
    "This message will be shown when the learner is browsing from an IP address that is not whitelisted.": "Este mensaje se mostrar\u00e1 cuando el estudiante est\u00e9 navegando desde una direcci\u00f3n IP que no est\u00e1 en la lista blanca.",
    "This message will be shown when the learner is prompted to enter the password.": "Este mensaje se mostrar\u00e1 cuando se pida al estudiante que introduzca la contrase\u00f1a.",
    "When enabled, the content will be restricted by IP address.": "Si esta opci\u00f3n est\u00e1 activa, entonces el contenido estar\u00e1 restringido por direcci\u00f3n IP.",
    "When enabled, the content will be restricted by password.": "Si esta opci\u00f3n est\u00e1 activa, entonces el contenido estar\u00e1 restringido por contrase\u00f1a.",
    "You are entering from an IP address that is not whitelisted. Please follow the instructions provided in the course introduction video.": "Est\u00e1 accediendo desde una direcci\u00f3n IP que no est\u00e1 en la lista blanca. Por favor, siga las instrucciones proporcionadas en el video de introducci\u00f3n del curso."
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
        