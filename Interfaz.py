# Lee los argumentos: tablero, normal o prueba
import time
import sys
import importlib.util
from Juego import Juego

def ImportLibrary( module_name, filename ):
  spec = importlib.util.spec_from_file_location( module_name, filename )
  if spec is None:
    print( f'Error: Could not create module specification for {filename}' )
    return None
  # end if
  module = importlib.util.module_from_spec( spec )
  sys.modules[ module_name ] = module
  try:
    spec.loader.exec_module( module )
    return module
  except Exception as e:
    print( f'Error executing module {filename}: {e}' )
    del sys.modules[ module_name ]
  # end try
  return None
# end def


def saludo() -> None:
    
    print("*" * 50)
    time.sleep(1)

    print("Bienvenido al juego :D \n")

    time.sleep(1)
    print("*" * 50)

    print()


# Lee los argumentos: tablero, jugador, normal o prueba
def main( script, argv ):
    if len( argv ) < 3:
        print( 'Uso: ' + script + ' tablero, jugador, prueba (false o true)' )
        sys.exit( 1 )
    
    tablero = argv[ 0 ].strip( )
    p = ImportLibrary( 'Player', argv[ 1 ] )
    prueba = argv[ 2 ].lower( ) == 'true'

    #Crear el jugador
    player = p.Player( )

    #Crear el juego
    juego = Juego( tablero, player, prueba )

    saludo()

    #Ejecutar el juego
    juego.solve( )

if __name__ == "__main__":
    main( sys.argv[ 0 ], sys.argv[ 1: ] )