import Tablero.tablero as tablero
class Player:

    '''
    '''
    m_Plays = None

    '''
    '''
    def __init__( self ):
        pass
    # end def

    '''
    '''
    def init( self, tablero ):
        self.m_Plays = []
        for r in range( h ):
            for c in range( w ):
                self.m_Plays += [ ( r, c ) ]
            # end for
        # end for
        random.shuffle( self.m_Plays )
    # end def

    '''
    '''
    def play( self ):
        return self.m_Plays.pop( 0 )
    # end def

    '''
    '''
    def report( self, response ):
        pass
    # end def

# end class

## eof - optimo.py
