# Recibe el tipo de jugador que quiere junto con su algoritmo


from Tablero import Tablero

"""
"""
class Juego:

    '''
    '''
    s_Tablero = None
    s_Player = None
    
    '''
    '''
    def __init__( self, name_tablero, player, prueba):
        self.s_Tablero = Tablero(name_tablero)
        self.s_Player = player;
        self.s_Player.init( self.s_Tablero )
    # end def

    '''
    '''
    def solve( self ):
        while not self.s_Tablero.finished( ):
            print( str( self.s_Tablero ) + '\n----------------------------' )
            p = self.s_Player.play( )
            r = self.s_Tablero.click( p )
            self.s_Player.report( r )
        # end while
        print( str( self.s_Tablero ) + '\n----------------------------' )
        if self.s_Tablero.finished( ):
            print( 'You won :-D' )

        # end if
    # end def
# end class

## eof - Game.py
