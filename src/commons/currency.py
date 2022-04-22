from django.db.models import TextChoices
from django.utils import numberformat
from django.utils.translation import gettext_lazy as _


class Currency(TextChoices):
    ARS = "ARS", _("ARS (Argentine peso)")
    BRL = "BRL", _("BRL (Brazilian real)")
    CLP = "CLP", _("CLP (Chilean peso)")
    COP = "COP", _("COP (Colombian peso)")
    CUP = "CUP", _("CUP (Cuban peso)")
    DOP = "DOP", _("DOP (Dominican peso)")
    MXN = "MXN", _("MXN (Mexican peso)")
    PHP = "PHP", _("PHP (Philippine peso)")
    USD = "USD", _("USD (United States dollar)")
    UYU = "UYU", _("UYU (Uruguayan peso)")


CURRENCY = {
    Currency.ARS: {
        "thousand_sep": ".",
        "decimal_sep": ",",
        "symbol": "$",
        "symbol_pos": "left",
    },
    Currency.BRL: {
        "thousand_sep": ".",
        "decimal_sep": ",",
        "symbol": "R$",
        "symbol_pos": "left",
    },
    Currency.CLP: {
        "thousand_sep": ",",
        "decimal_sep": ".",
        "symbol": "$",
        "symbol_pos": "left",
    },
    Currency.COP: {
        "thousand_sep": ",",
        "decimal_sep": ".",
        "symbol": "$",
        "symbol_pos": "left",
    },
    Currency.CUP: {
        "thousand_sep": ",",
        "decimal_sep": ".",
        "symbol": "$",
        "symbol_pos": "left",
    },
    Currency.DOP: {
        "thousand_sep": ",",
        "decimal_sep": ".",
        "symbol": "$",
        "symbol_pos": "left",
    },
    Currency.MXN: {
        "thousand_sep": ",",
        "decimal_sep": ".",
        "symbol": "$",
        "symbol_pos": "right",
    },
    Currency.PHP: {
        "thousand_sep": ",",
        "decimal_sep": ".",
        "symbol": "₱",
        "symbol_pos": "left",
    },
    Currency.USD: {
        "thousand_sep": ",",
        "decimal_sep": ".",
        "symbol": "$",
        "symbol_pos": "left",
    },
    Currency.UYU: {
        "thousand_sep": ",",
        "decimal_sep": ".",
        "symbol": "$",
        "symbol_pos": "left",
    },
}


def format(value, currency):  # noqa
    """
    Format a given value into a currency definition.
    """
    format_ = CURRENCY.get(currency) or {}
    symbol = format_.get("symbol", "$")
    symbol_pos = format_.get("symbol_pos", "left")
    decimal_sep = format_.get("decimal_sep", ".")
    thousand_sep = format_.get("thousand_sep", ",")

    value = numberformat.format(
        value,
        decimal_sep=decimal_sep,
        thousand_sep=thousand_sep,
        decimal_pos=2,
        grouping=3,
        force_grouping=True,
        use_l10n=True,
    )

    value = f"{value} {symbol}" if symbol_pos == "right" else f"{symbol} {value}"

    return value
