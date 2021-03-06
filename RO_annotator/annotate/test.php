<?php

require_once "lib/lib.php";
require_once "steps/1_basic_tagging.php";
require_once "steps/2_iate_eurovoc.php";
require_once "steps/3_cleanup.php";
require_once "steps/4_eurovoc_class.php";
require_once "steps/5_export_marcell.php";


$text="Se aprobă publicarea Tabloului executorilor judecătorești pentru anul 2020 în Monitorul Oficial al României, Partea I, prevăzut în anexa care face parte integrantă din prezenta hotărâre.";
$meta=<<<EOT
<root>
 <Metadata>
<DocumentTitle>RAPORT 4393 11/03/2019</DocumentTitle>
<ArticleTitle>RAPORT 4393 11/03/2019</ArticleTitle>
<AuthorName>-</AuthorName>
<PublicationDate>2019</PublicationDate>
<Source>Website</Source>
<SourceName>http://legislatie.just.ro/Public/FormaPrintabila/00000G0004U3GHG6INE11CXTOEQ9RL5L</SourceName>
<TranslatorName>-</TranslatorName>
 <Medium>Written</Medium>
<DocumentType>RAPORT</DocumentType>
<NewDocId>ro-00000G0004U3GHG6INE11CXTOEQ9RL5L</NewDocId>
<DocumentTextStyle>Law</DocumentTextStyle>
 <DocumentTextDomain>-</DocumentTextDomain>
 <DocumentTextSubdomain>-</DocumentTextSubdomain>
 <CollectionDate>2018</CollectionDate>
 <SubjectLanguage>ro</SubjectLanguage>
 <IssnIsbn>-</IssnIsbn>
 </Metadata>
 </root>
EOT;

$docid="mj_XXXXXX";

$columns="# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC MARCELL:NE MARCELL:NP MARCELL:IATE MARCELL:EUROVOC";

echo "***********************************\n";
echo "STEP 1\n";
$ann=runBasicTaggingText_ro($text);
var_dump($ann);
echo "\n\n\n";

echo "***********************************\n";
echo "STEP 2\n";
$ann=runIateEurovoc_internal($ann);
$ann=$columns."\n".$ann;
var_dump($ann);
echo "\n\n\n";

echo "***********************************\n";
echo "STEP 3\n";
$ann=cleanFileContent($ann,"");
var_dump($ann);
echo "\n\n\n";

echo "***********************************\n";
echo "STEP 4\n";
$ann=runEurovocClass($ann);
var_dump($ann);
echo "\n\n\n";


echo "***********************************\n";
echo "STEP 5\n";
$java="/ner/jdk1.8.0_191/bin/java";
//$java="/data/programs/jdk1.8.0_231/bin/java";
$tmpfolder=uniqid("r",true);
@mkdir("corrector/$tmpfolder");
@mkdir("corrector/$tmpfolder/text");
file_put_contents("corrector/$tmpfolder/text/$docid.txt",$ann);
@mkdir("corrector/$tmpfolder/standoff");
file_put_contents("corrector/$tmpfolder/standoff/$docid.xml",$meta);
$ann=runExportMarcell($java,$tmpfolder);
passthru("rm -fr corrector/$tmpfolder");
var_dump($ann);
echo "\n\n\n";
