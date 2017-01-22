import os
import sys
import subprocess
import shlex

#Variaveis globais
CaminhoArquivoControle="/tmp/ControleRadio"
ComandoMPlayer = "mplayer -input file=/tmp/ControleRadio -slave -playlist "

#Variaveis das playlists
Playlists=[]        #Array que contem todas as playlists
NumeroPlaylists = 0 #quantidade de playlists
NomesRadios=[]      #Nomes das radios / playlists
PlaylistEscolhida=0 #Indice da playlist escolhida

NomeRadio1="Radio ShoutCast"
NomeRadio2="Radio Backstage (www.radiobackstage.com)"

#Funcao: inicia lista de playlists
#Parametros: nenhum
#Retorno: nenhum
def IniciaListaPlaylists():
	global Playlists
	global NomesRadios
	global NumeroPlaylists

	#playlist 1
	Playlists.append("http://yp.shoutcast.com/sbin/tunein-station.pls?id=1057392")
	NomesRadios.append("Radio Shoutcast")

	#playlist 2
	Playlists.append("http://panel3.serverhostingcenter.com:2199/tunein/radiobackstage1.pls")
	NomesRadios.append("Radio Backstage")

	#playlist 3
	Playlists.append("http://yp.shoutcast.com/sbin/tunein-station.pls?id=1425714")
	NomesRadios.append("Techno")

	NumeroPlaylists=3
	return

#Funcao: Toca a plsylist escolhida
#Parametros: nenhum
#Retorno: nenhum
def TocaPlaylist(PEscolhida):
	global Playlists
	global ComandoMPlayer

	os.system("pkill -f mplayer")
	ComandoPlaylist = ComandoMPlayer + Playlists[PEscolhida]
	
	#inicia processo e direciona o stdout para /dev/null
	FNULL = open(os.devnull,'w')
	args = shlex.split(ComandoPlaylist)
	InterfaceMPlayer = subprocess.Popen(args, shell=False, stdin=subprocess.PIPE, stdout=FNULL, stderr=subprocess.STDOUT)

	#ajusta volume em 50%
	os.system('echo "volume 50" >'+CaminhoArquivoControle)

	return


#Funcao: cria arquivo de controle do player (MPlayer)
#Parametros: nenhum
#Retorno: nenhum
def CriaArquivoControle():
	#se arquivo ja existe, nada e feito.
	if (os.path.exists(CaminhoArquivoControle)):
		return

	try:
		os.mkfifo(CaminhoArquivoControle)
	except:
		print "Falha ao criar arquivo de controle. Por favor, verifique o caminho de criacao do mesmo."
		exit(1)

#Funcao: escreve na tela o menu de opcoes
#Parametros: nenhum
#Retorno:  opcao escolhida
def MostraMenuDeOpcoes():
	global NomesRadios
	global PlaylitsEscolhida

	print "-----------------------"
	print "    Menu de opcoes     "
	print "-----------------------"
	print "Estacao: "+NomesRadios[PlaylistEscolhida]
	print " "
	print "<p> Play/pause"
	print "<s> Sair"
	print "<+> Sobe volume"
	print "<-> Desce volume"
	print "<d> Proxima estacao"
	print "<a> Estacao anterior"
	print " "
	opcao = raw_input("Opcao> ")

	return opcao


#------------------
#Programa principal
#------------------

#Inicializa lista de playlists
IniciaListaPlaylists()

#Cria arquivo de controle e inicia processo MPlayer
CriaArquivoControle()

#Toca playlist 1
TocaPlaylist(PlaylistEscolhida)

while True:
	try:
		os.system("clear")
		Tecla = MostraMenuDeOpcoes()

		if (Tecla == "p"):
			print "[ACAO] Play/Pause"
			os.system('echo "pause" > '+CaminhoArquivoControle)

		if (Tecla == "s"):
			print "[ACAO] Sair"
			os.system('echo "quit 0" > '+CaminhoArquivoControle)
			os.system("pkill -f mplayer")
			exit(1)

		if (Tecla == "+"):
			print "[ACAO] Sobe volume"
			os.system('echo "volume +10" > '+CaminhoArquivoControle)

		if (Tecla == "-"):
			print "[ACAO] Desce volume"
			os.system('echo "volume -10" > '+CaminhoArquivoControle)

		if (Tecla == "d"):
			print "[ACAO] Proxima estacao"
			PlaylistEscolhida = PlaylistEscolhida + 1
			if (PlaylistEscolhida == NumeroPlaylists):
				PlaylistEscolhida = 0
			TocaPlaylist(PlaylistEscolhida)

		if (Tecla == "a"):
			print "[ACAO] Estacao anterior"
			PlaylistEscolhida = PlaylistEscolhida - 1
			if (PlaylistEscolhida < 0):
				PlaylistEscolhida = NumeroPlaylists-1
			TocaPlaylist(PlaylistEscolhida)


	except (KeyboardInterrupt):
		print "Aplicacao sendo encerrada."
		exit(1)
