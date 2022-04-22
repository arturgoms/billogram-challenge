import calendar
import datetime


MO, TU, WE, TH, FR, SA, SU = range(1, 8)


def week_range(dt, ws=SU):
    """
    Find the first and last days of the reference date week.
    Returns a tuple of ``(start_date, end_date)``.

    Parameters:
        dt (datetime.date, required): Reference date.
        ws (int, optional): Tells witch day will be used as the Week Start;

    Returns:
        (datetime.date, datetime.date)
    """
    # iso-calendar calculates the year, week of the year, and day of the week.
    # day of week is MO = 1, ... SA = 6, SU = 7
    _, _, dow = dt.isocalendar()

    # calculate the week start date based on dow and week_start
    start_date = dt - datetime.timedelta(days=dow - ws if dow >= ws else 7 - (ws - dow))

    # calculate the week end date based on start_date
    end_date = start_date + datetime.timedelta(days=6)

    return start_date, end_date


def month_range(dt):
    """
    Returns the first and last days of the reference date month.

    Returns a tuple of ``(start_date, end_date)``.

    Parameters:
        dt (datetime.date, required): Reference date;

    Returns:
        (datetime.date, datetime.date)
    """
    _, last_day = calendar.monthrange(dt.year, dt.month)
    return dt.replace(day=1), dt.replace(day=last_day)
