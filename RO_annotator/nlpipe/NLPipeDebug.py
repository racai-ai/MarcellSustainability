from multiprocessing import freeze_support
from PipAlgo import PipAlgo
from NLPipe import NLPipe
import platform
import json

def main():
    # How to use the NLPipe Python 3 object:
    # 1. Create the object
    pipe = NLPipe()

    # 2. Optionally, configure the operation execution
    # Example configuration call
    pipe.configure(PipAlgo.getSentenceSplittingOperName(), PipAlgo.algoTTL)
    pipe.configure(PipAlgo.getTokenizationOperName(), PipAlgo.algoTTL)
    pipe.configure(PipAlgo.getPOSTaggingOperName(), PipAlgo.algoTTL)
    pipe.configure(PipAlgo.getLemmatizationOperName(), PipAlgo.algoTTL)

    # 2.1 Test biomedical NER
    text = "Diabetul zaharat este un sindrom caracterizat prin valori crescute ale concentrației glucozei în sânge (hiperglicemie) și dezechilibrarea metabolismului."
    dto = pipe.pcExec(
        text, [PipAlgo.getBiomedicalNamedEntityRecognitionOperName()])
    dto.dumpConllX()

    # 2.2 Test NER
    text = "Instanta suprema reia astazi judecarea. In dosar, se judeca Liviu Dragnea cu Ministerul Justitiei, condus de Tudorel Toader."
    dto = pipe.pcExec(text, [PipAlgo.getNamedEntityRecognitionOperName()])
    dto.dumpConllX()

    # 2.3 Test for some bugs
    text = "Am aflat aprope ca euro si dolarul sunt cele mai bune."
    dto = pipe.pcFull(text)
    dto.dumpConllX()

    text = "Stia ca demonstratia o sa fie un succes."
    dto = pipe.pcFull(text)
    dto.dumpConllX()

    # 2.4 Test for a crash
    text = "Președintele Klaus Iohannis a anunțat că nu promulgă legea bugetului pe 2019 și sesizează Curtea Constituțională. " + \
        "„Este bugetul rușinii naționale”, a spus șeful statului care a acuzat PSD că e incapabil să guverneze pentru România, singura preocupare fiind Liviu Dragnea.\n\n" + \
        "„Un lucru este clar, Guvernarea PSD a eșuat. În spitale, probleme peste probleme Educația este subfinanțată. " + \
        "România este bulversată mai ales după OUG 114, dată în mare taină la finalul anului trecut. " + \
        "Despre justiție, întreaga guvernare pesedistă a fost un asalt asupra statului de drept din România. PSD e incapabil să conducă România. " + \
        "PSD nu guvernează pentru români, PSD guvernează pentru Dragnea”, a spus Iohannis.\n\n" + \
        "Referindu-se la bugetul pe 2019, șeful statului a spus că acesta este „nerealist și supraevaluat”, calificându-l drept unul al „rușinii naționale”.\n\n" + \
        "Președintele a acuzat PSD că nu are bani de investiții, dar are bani pentru partid. " + \
        "„150 de milioane va primi PSD din finanțarea partidelor, din 270 de milioane propuse pentru finanțarea partidelor. " + \
        "PSD și-a tras bani de 20 de ori mai mult decât anul trecut (președinția a precizat ulterior că această comparație a fost făcută cu 2016 - n.r.). " + \
        "Pentru asta au bani”, a spus Iohannis.\n"
    dto = pipe.pcFull(text)
    dto.dumpConllX()

    text = "HotNews.ro transmite LIVETEXT cele mai importante declarații din cadrul audierilor\n\n" + \
        "Ora 17,00: Andres Ritter, candidatul Germaniei a vorbit despre necesitatea înființării Parchetului European în contextul fraudelor și corupției, " + \
        "care slăbesc credibilitatea UE în ochii contribuabililor. În opinia sa, abordarea la nivel național nu a fost suficientă, este necesară o " + \
        "abordare unitară la nivelul UE\n\n" + \
        "Ora 16:40 S-a stabilit ordinea audierilor, prin tragere la sorți: " + \
        "Primul va fi audiat candidatul Germaniei, Andrés Ritter (54 de ani), urmat de candidatul Franței, " + \
        "Jean-François Bohnert (58 de ani) și de Laura Codruța Kovesi.\n"
    dto = pipe.pcFull(text)
    dto.dumpConllX()

    text = "La 7      minute de centrul Brasovului,  imobilul\tpropus \
        spre vanzare se adreseaza\t\tcelor care isi doresc un spatiu \
        generos de locuit.\n\nAmplasarea constructiei  si\t\tgarajul reusesc sa exploateze \
        la maxim lotul de teren de 670 mp, ce are o deschidere de 15 ml.\n"

    # 3. Call one of the already created 'processing chains' ('pc' for short)
    # or call the generic pcExec method.
    # Example 1: using a canned processing chain ('pc'), e.g. diacritics insertion.
    dto = pipe.pcDiac(text)
    print(dto.getText())

    # Example 2: using another canned pc, e.g. lemmatization.
    dto = pipe.pcLemma(text)
    print(json.dumps(dto.jsonDict(), default=lambda x: x.__dict__))

# Do this on Windows, if multiprocessing is used down the call chain.
# To debug in MS Visual Studio 2017, add if __name__ statement in all modules where
# multiprocessing is used down the call chain. 
# See https://docs.python.org/3/library/multiprocessing.html, freeze_support()
if __name__ == "__main__":
    if platform.system() == "Windows":
        freeze_support()

    main()
