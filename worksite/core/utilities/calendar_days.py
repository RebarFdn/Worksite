# Standard library
import calendar
# Third party
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
# Constants
COLOR = "#FC5200"
OFFSET = 0.5

def prepare_axes(ax):
    ax.set(aspect=1, xlim=(0, 7), ylim=(0, 7))
    ax.axis("off")
    return ax

def place_text(ax, x, y, text):
    ax.text(x + OFFSET, y + OFFSET, s=text,
            ha="center", va="center", color=COLOR)

def label_weekday(ax):
    top_row_position = 6
    for day_number, weekday in enumerate(calendar.day_abbr):
        place_text(ax=ax, x=day_number, y=top_row_position, text=weekday[0])

def draw_circle(ax, x_pos, y_pos):
    ax.add_artist(
        mpatches.Circle(
            (x_pos + OFFSET, y_pos + OFFSET), radius=0.45,
            edgecolor=COLOR, facecolor="None"))

def draw_calendar_of_a_month(ax, first, num_days):
    ax = prepare_axes(ax)
    label_weekday(ax)
    x_pos = first
    y = 5
    for day in range(1, num_days + 1):
        draw_circle(ax, x_pos, y)
        place_text(ax, x_pos, y, day)
        x_pos = (x_pos + 1) % 7
        if x_pos == 0:
            y -= 1

# Plot June 2025 the month that spans six calendar weeks
fig = plt.figure()
ax = fig.add_subplot()
first_day, number_of_days = calendar.monthrange(2025, 6)
draw_calendar_of_a_month(ax, first_day, number_of_days)
plt.show()


#_______________

def place_text(ax, x, y, text, highlighted=False):  # default parameter
    ax.text(x + OFFSET, y + OFFSET, s=text,
            ha="center", va="center",
            # default is COLOR, otherwise use face color is hightlighted is True
            color=COLOR if not highlighted else ax.get_facecolor())

def draw_circle(ax, x_pos, y_pos, highlight=False):  # default parameter
    ax.add_artist(
        mpatches.Circle(
            (x_pos + OFFSET, y_pos + OFFSET), radius=0.45,
            # default is no color, otherwise use COLOR
            edgecolor=COLOR, facecolor=COLOR if highlight else "None"))


def draw_calendar_of_a_month(ax, first, num_days, highlights):  # additional parameter
    ax = prepare_axes(ax)
    label_weekday(ax)
    x_pos = first
    y = 5
    for day in range(1, num_days + 1):
        # set a highlight boolean
        highlight: bool = day in highlights if highlights else False
        draw_circle(ax, x_pos, y, highlight)  # provide argument
        place_text(ax, x_pos, y, day, highlighted=highlight)  # provide argument
        x_pos = (x_pos + 1) % 7
        if x_pos == 0:
            y -= 1

active_days = [5, 6, 7, 10, 27]
draw_calendar_of_a_month(ax, first_day, number_of_days, active_days)


def place_icon(ax, activity, x_pos, y):
    icons = {
        "bike": pytablericons.OutlineIcon.BIKE,
        "run": pytablericons.OutlineIcon.RUN,
        "swim": pytablericons.OutlineIcon.SWIMMING,
        "weight": pytablericons.OutlineIcon.BARBELL
    }
    padding = .02
    newax = ax.inset_axes([x_pos / 7 + padding, y / 7 + padding, .1, .1])
    icon = icons.get(activity) or pytablericons.OutlineIcon.BOLT
    newax.imshow(pytablericons.TablerIcons.load(icon))
    newax.axis('off')

def draw_calendar_of_a_month(ax, first, num_days, highlights=None, activities=None, show_icon=False):
    ax = prepare_axes(ax)
    label_weekday(ax)
    x_pos = first
    y = 5

    for day in range(1, num_days + 1):
        highlight = day in highlights if highlights else False
        draw_circle(ax, x_pos, y, highlight)
        # Either place an icon or text based on the hightlight value
        if show_icon and day in highlights:
            place_icon(ax, activities.pop(0) if activities else None, x_pos, y)
        else:
            place_text(ax, x_pos, y, day, highlighted=highlight)
        x_pos = (x_pos + 1) % 7
        if x_pos == 0:
            y -= 1