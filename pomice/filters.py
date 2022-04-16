from typing import Union

from exceptions import FilterInvalidArgument


class Filter:
    """
    The base class for all filters.
    You can use these filters if you have the latest Lavalink version
    installed. If you do not have the latest Lavalink version,
    these filters will not work.
    """

    name = None

    def __init__(self):
        self.payload = None

    def edit(self, key: str, value: Union[int, float]):

        if not isinstance(key, str):
            raise TypeError(f"Key must be a string not ({key!r})")

        if not self.name:
            raise ValueError("Filter must have a name.")

        self.payload[self.name][key] = value

    def _reset(self):
        raise NotImplementedError


class Equalizer(Filter):
    """
    Filter which represents a 15 band equalizer.
    You can adjust the dynamic of the sound using this filter.
    i.e: Applying a bass boost filter to emphasize the bass in a song.
    The format for the levels is: List[Tuple[int, float]]
    """

    name = "equalizer"

    def __init__(self, *, levels: list):
        super().__init__()

        self.eq = self._format(levels)
        self.raw = levels

        self.payload = {"eqalizer": self.eq}

    @staticmethod
    def _format(levels: list):
        data = [{'band': band, 'gain': gain}
                for band, gain in levels]

        return data

    def _reset(self):
        self.raw = [(0, .0), (1, .0), (2, .0), (3, .0), (4, .0),
                    (5, .0), (6, .0), (7, .0), (8, .0), (9, .0),
                    (10, .0), (11, .0), (12, .0), (13, .0), (14, .0)]

        self.eq = self._format(levels=self.raw)
        self.payload = {"equalizer": self.eq}

        return self.payload

    def __repr__(self) -> str:
        return f"<Pomice.EqualizerFilter eq={self.eq} raw={self.raw}>"


class Timescale(Filter):
    """Filter which changes the speed and pitch of a track.
       You can make some very nice effects with this filter,
       i.e: a vaporwave-esque filter which slows the track down
       a certain amount to produce said effect.
    """

    name = "timescale"

    def __init__(
        self,
        *,
        speed: float = 1.0,
        pitch: float = 1.0,
        rate: float = 1.0
    ):
        super().__init__()

        if speed < 0:
            raise FilterInvalidArgument("Timescale speed must be more than 0.")
        if pitch < 0:
            raise FilterInvalidArgument("Timescale pitch must be more than 0.")
        if rate < 0:
            raise FilterInvalidArgument("Timescale rate must be more than 0.")

        self.speed = speed
        self.pitch = pitch
        self.rate = rate

        self.payload = {"timescale": {"speed": self.speed,
                                      "pitch": self.pitch,
                                      "rate": self.rate}}

    def _reset(self):
        self.speed = 1.0
        self.pitch = 1.0
        self.rate = 1.0

        self.payload = {"timescale": {"speed": self.speed,
                                      "pitch": self.pitch,
                                      "rate": self.rate}}

        return self.payload

    def __repr__(self):
        return f"<Pomice.TimescaleFilter speed={self.speed} pitch={self.pitch} rate={self.rate}>"


class Karaoke(Filter):
    """Filter which filters the vocal track from any song and leaves the instrumental.
       Best for karaoke as the filter implies.
    """

    name = "karaoke"

    def __init__(
        self,
        *,
        level: float = 1.0,
        mono_level: float = 1.0,
        filter_band: float = 220.0,
        filter_width: float = 100.0
    ):
        super().__init__()

        self.level = level
        self.mono_level = mono_level
        self.filter_band = filter_band
        self.filter_width = filter_width

        self.payload = {"karaoke": {"level": self.level,
                                    "monoLevel": self.mono_level,
                                    "filterBand": self.filter_band,
                                    "filterWidth": self.filter_width}}

    def _reset(self):
        self.level: float = 1.0
        self.mono_level: float = 1.0
        self.filter_band: float = 220.0
        self.filter_width: float = 100.0

        self.payload = {"karaoke": {"level": self.level,
                                    "monoLevel": self.mono_level,
                                    "filterBand": self.filter_band,
                                    "filterWidth": self.filter_width}}

        return self.payload

    def __repr__(self):
        return (
            f"<Pomice.KaraokeFilter level={self.level} mono_level={self.mono_level} "
            f"filter_band={self.filter_band} filter_width={self.filter_width}>"
        )


class Tremolo(Filter):
    """Filter which produces a wavering tone in the music,
       causing it to sound like the music is changing in volume rapidly.
    """

    name = "tremolo"

    def __init__(
        self,
        *,
        frequency: float = 2.0,
        depth: float = 0.5
    ):
        super().__init__()

        if frequency < 0:
            raise FilterInvalidArgument(
                "Tremolo frequency must be more than 0.")
        if depth < 0 or depth > 1:
            raise FilterInvalidArgument(
                "Tremolo depth must be between 0 and 1.")

        self.frequency = frequency
        self.depth = depth

        self.payload = {"tremolo": {"frequency": self.frequency,
                                    "depth": self.depth}}

    def _reset(self):
        self.frequency: float = 2.0
        self.depth: float = 0.5

        self.payload = {"tremolo": {"frequency": self.frequency,
                                    "depth": self.depth}}

        return self.payload

    def __repr__(self):
        return f"<Pomice.TremoloFilter frequency={self.frequency} depth={self.depth}>"


class Vibrato(Filter):
    """Filter which produces a wavering tone in the music, similar to the Tremolo filter,
       but changes in pitch rather than volume.
    """

    name = "vibrato"

    def __init__(
        self,
        *,
        frequency: float = 2.0,
        depth: float = 0.5
    ):

        super().__init__()
        if frequency < 0 or frequency > 14:
            raise FilterInvalidArgument(
                "Vibrato frequency must be between 0 and 14.")
        if depth < 0 or depth > 1:
            raise FilterInvalidArgument(
                "Vibrato depth must be between 0 and 1.")

        self.frequency = frequency
        self.depth = depth

        self.payload = {"vibrato": {"frequency": self.frequency,
                                    "depth": self.depth}}

    def _reset(self):
        self.frequency: float = 2.0
        self.depth: float = 0.5

        self.payload = {"vibrato": {"frequency": self.frequency,
                                    "depth": self.depth}}

        return self.payload

    def __repr__(self):
        return f"<Pomice.VibratoFilter frequency={self.frequency} depth={self.depth}>"


class Rotation(Filter):
    """Filter which produces a stereo-like panning effect, which sounds like
    the audio is being rotated around the listener's head
    """

    name = "rotation"

    def __init__(self, *, rotation_hertz: float = 5):
        super().__init__()

        self.rotation_hertz = rotation_hertz

        self.payload = {"rotation": {"rotationHz": self.rotation_hertz}}

    def _reset(self):
        self.rotation_hertz = 5
        self.payload = {"rotation": {"rotationHz": self.rotation_hertz}}

        return self.payload

    def __repr__(self) -> str:
        return f"<Pomice.RotationFilter rotation_hertz={self.rotation_hertz}>"


class ChannelMix(Filter):
    """Filter which manually adjusts the panning of the audio, which can make
    for some cool effects when done correctly.
    """

    name = "channelMix"

    def __init__(
        self,
        *,
        left_to_left: float = 1,
        right_to_right: float = 1,
        left_to_right: float = 0,
        right_to_left: float = 0
    ):
        super().__init__()

        if 0 > left_to_left > 1:
            raise ValueError(
                "'left_to_left' value must be more than or equal to 0 or less than or equal to 1.")
        if 0 > right_to_right > 1:
            raise ValueError(
                "'right_to_right' value must be more than or equal to 0 or less than or equal to 1.")
        if 0 > left_to_right > 1:
            raise ValueError(
                "'left_to_right' value must be more than or equal to 0 or less than or equal to 1.")
        if 0 > right_to_left > 1:
            raise ValueError(
                "'right_to_left' value must be more than or equal to 0 or less than or equal to 1.")

        self.left_to_left = left_to_left
        self.left_to_right = left_to_right
        self.right_to_left = right_to_left
        self.right_to_right = right_to_right

        self.payload = {"channelMix": {"leftToLeft": self.left_to_left,
                                       "leftToRight": self.left_to_right,
                                       "rightToLeft": self.right_to_left,
                                       "rightToRight": self.right_to_right}
                        }

    def _reset(self):
        self.left_to_left: float = 1
        self.right_to_right: float = 1
        self.left_to_right: float = 0
        self.right_to_left: float = 0

        self.payload = {"channelMix": {"leftToLeft": self.left_to_left,
                                       "leftToRight": self.left_to_right,
                                       "rightToLeft": self.right_to_left,
                                       "rightToRight": self.right_to_right}
                        }

        return self.payload

    def __repr__(self) -> str:
        return (
            f"<Pomice.ChannelMix left_to_left={self.left_to_left} left_to_right={self.left_to_right} "
            f"right_to_left={self.right_to_left} right_to_right={self.right_to_right}>"
        )


class Distortion(Filter):
    """Filter which generates a distortion effect. Useful for certain filter implementations where
    distortion is needed. 
    """

    name = "distortion"

    def __init__(
        self,
        *,
        sin_offset: float = 0,
        sin_scale: float = 1,
        cos_offset: float = 0,
        cos_scale: float = 1,
        tan_offset: float = 0,
        tan_scale: float = 1,
        offset: float = 0,
        scale: float = 1
    ):
        super().__init__()

        self.sin_offset = sin_offset
        self.sin_scale = sin_scale
        self.cos_offset = cos_offset
        self.cos_scale = cos_scale
        self.tan_offset = tan_offset
        self.tan_scale = tan_scale
        self.offset = offset
        self.scale = scale

        self.payload = {"distortion": {
            "sinOffset": self.sin_offset,
            "sinScale": self.sin_scale,
            "cosOffset": self.cos_offset,
            "cosScale": self.cos_scale,
            "tanOffset": self.tan_offset,
            "tanScale": self.tan_scale,
            "offset": self.offset,
            "scale": self.scale
        }}

    def _reset(self):
        self.sin_offset: float = 0
        self.sin_scale: float = 1
        self.cos_offset: float = 0
        self.cos_scale: float = 1
        self.tan_offset: float = 0
        self.tan_scale: float = 1
        self.offset: float = 0
        self.scale: float = 1

        self.payload = {"distortion": {
            "sinOffset": self.sin_offset,
            "sinScale": self.sin_scale,
            "cosOffset": self.cos_offset,
            "cosScale": self.cos_scale,
            "tanOffset": self.tan_offset,
            "tanScale": self.tan_scale,
            "offset": self.offset,
            "scale": self.scale
        }}

        return self.payload

    def __repr__(self) -> str:
        return (
            f"<Pomice.Distortion sin_offset={self.sin_offset} sin_scale={self.sin_scale}> "
            f"cos_offset={self.cos_offset} cos_scale={self.cos_scale} tan_offset={self.tan_offset} "
            f"tan_scale={self.tan_scale} offset={self.offset} scale={self.scale}"
        )


class LowPass(Filter):
    """Filter which supresses higher frequencies and allows lower frequencies to pass.
    You can also do this with the Equalizer filter, but this is an easier way to do it.
    """

    name = "lowPass"

    def __init__(self, *, smoothing: float = 20):
        super().__init__()

        self.smoothing = smoothing

        self.payload = {"lowPass": {"smoothing": self.smoothing}}

    def _reset(self):
        self.smoothing = 20
        self.payload = {"lowPass": {"smoothing": self.smoothing}}

        return self.payload

    def __repr__(self) -> str:
        return f"<Pomice.LowPass smoothing={self.smoothing}>"


class CustomFilter(Filter):
    """Filter which allows you to stack Filters and this only accepts Filters
    subclassed from `Filters` class"""

    name = "customFilter"

    def __init__(self, *filters: Filter):
        super().__init__()

        self._filters = {}

        for filter in filters:
            if not isinstance(filter, Filter):
                raise TypeError(
                    f"filter must be subclassed from <pomice.Filter> not {filter!r}")

            self._filters[filter.__class__.__name__] = filter

    @property
    def filters(self):
        """Return all the Filters currently being used."""
        return self._filters

    def add_filter(self, *filters: Filter):
        """Add a Filter to CustomFilter and if the Filter already
        exists then it is skipped."""

        for filter in filters:
            if not isinstance(filter, Filter):
                raise TypeError(
                    f"filter must be subclassed from <pomice.Filter> not {filter!r}")

            if (name := filter.__class__.__name__) not in filters:
                self._filters[name] = filter

    def get_payload(self):
        """Get the combined payload from `CustomFilter._filters`."""

        data = {}
        for value in self._filters.values():
            data.update(value.payload)

        return data

    def edit(self, filter: Union[Filter, str], key: str, value: Union[int, float]):
        """Edit a Filter within the Custom Filters
        `filter` must be of either the class itself or the name of the class
        eg:

        CustomFilter.edit(Distortion, key, value)
        or
        CustomFilter.edit("Distortion", key, value)
        """

        if isinstance(filter, str):
            name = filter
        elif issubclass(filter, Filter):
            name = filter.__name__
        else:
            raise TypeError("`filter` argument must be of `Filter` or `str`")

        if name not in self._filters:
            raise KeyError(
                f"({name}) does not exist in ({', '.join(k for k in self._filters)})")

        self._filters[name].edit(key, value)

    def reset(self, *filters: Filter):
        """Reset a specific Filter or all Filters."""

        if not filters:
            filters_reset = self._filters.values()
        else:
            filters_reset = (filter for filter in self.filters.values()
                             if filter.__class__ in filters)

        data = {}
        for filter in filters_reset:
            data.update(filter._reset())

        return data
    
