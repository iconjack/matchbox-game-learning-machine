class Nim():
    def __init__(self, initpile, maxtake=3):
        self.initpile = initpile
        self.maxtake = maxtake

    # state of game is pilesize
    def __getitem__(self, pilesize):
        if pilesize is None:             # not the same as pilesize == 0
            return self.initpile
        else:
            return range(max(pilesize-self.maxtake, 0), pilesize)