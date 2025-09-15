from pytubefix import YouTube
from pytubefix.cli import on_progress
from pathlib import Path

# === Inserir o link manualmente ===
url = input("Cole aqui o link do vídeo do YouTube: ").strip()

# Pasta de destino
destino = Path("pasta_video")
destino.mkdir(exist_ok=True)

# Criar objeto YouTube
yt = YouTube(url, on_progress_callback=on_progress)
print(f"\n🎬 Título: {yt.title}\n⏱️ Duração: {yt.length}s")

# ==== MENU PRINCIPAL ====
print("\nO que deseja baixar?")
print("1 - Vídeo com áudio (MP4 progressivo)")
print("2 - Somente vídeo (sem áudio)")
print("3 - Somente áudio")

opcao_principal = int(input("\nEscolha a opção desejada: "))

# ==== OPÇÃO 1: Vídeo com áudio ====
if opcao_principal == 1:
    streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()
    print("\nQualidades disponíveis (vídeo + áudio):")
    for i, stream in enumerate(streams, start=1):
        print(f"{i}: {stream.resolution} - {round(stream.filesize / 1024 / 1024, 2)} MB")
    escolha = int(input("\nEscolha a qualidade: "))
    escolhido = streams[escolha - 1]
    print(f"\n⬇️ Baixando {escolhido.resolution}...")
    escolhido.download(output_path=destino)

# ==== OPÇÃO 2: Somente vídeo ====
elif opcao_principal == 2:
    streams = yt.streams.filter(only_video=True, file_extension="mp4").order_by("resolution").desc()
    print("\nQualidades disponíveis (apenas vídeo, sem áudio):")
    for i, stream in enumerate(streams, start=1):
        print(f"{i}: {stream.resolution} - {stream.mime_type} - {round(stream.filesize / 1024 / 1024, 2)} MB")
    escolha = int(input("\nEscolha a qualidade: "))
    escolhido = streams[escolha - 1]
    print(f"\n⬇️ Baixando {escolhido.resolution} (vídeo sem áudio)...")
    escolhido.download(output_path=destino)

# ==== OPÇÃO 3: Somente áudio ====
elif opcao_principal == 3:
    streams = yt.streams.filter(only_audio=True).order_by("abr").desc()
    print("\nQualidades disponíveis (áudio):")
    for i, stream in enumerate(streams, start=1):
        print(f"{i}: {stream.abr} - {stream.mime_type} - {round(stream.filesize / 1024 / 1024, 2)} MB")
    escolha = int(input("\nEscolha a qualidade: "))
    escolhido = streams[escolha - 1]
    print(f"\n⬇️ Baixando áudio {escolhido.abr}...")
    escolhido.download(output_path=destino, filename=f"{yt.title}.mp3")

else:
    print("❌ Opção inválida!")

print(f"\n✅ Download concluído! Arquivo salvo em: {destino}")
