<?php

registerHandler("home/home","pages/home/home.php",false);


registerHandler("platform/login","pages/platform/login.php",false);
registerHandler("platform/register","pages/platform/register.php",false);
registerHandler("platform/logout","pages/platform/logout.php",false);
registerHandler("platform/change_password","pages/platform/change_password.php",false);

registerHandler("downloads/private","pages/downloads/private.php",false,["user"]);
registerHandler("downloads/data","pages/downloads/data.php",true);

registerHandler("corpus/list","pages/corpus/list.php",false,["corpus"]);
registerHandler("corpus/list_get","pages/corpus/list_get.php",true,["corpus"]);
registerHandler("corpus/list_add","pages/corpus/list_add.php",true,["corpus"]);
registerHandler("corpus/corpus","pages/corpus/corpus.php",false,["corpus"]);
registerHandler("corpus/files_get","pages/corpus/files_get.php",true,["corpus"]);
registerHandler("corpus/files_getbasictagging","pages/corpus/files_getbasictagging.php",true,["corpus"]);
registerHandler("corpus/files_getstandoff","pages/corpus/files_getstandoff.php",true,["corpus"]);
registerHandler("corpus/stats_get","pages/corpus/stats_get.php",true,["corpus"]);
registerHandler("corpus/files_add","pages/corpus/files_add.php",true,["corpus"]);
registerHandler("corpus/csv_view","pages/corpus/csv_view.php",false,["corpus"]);
registerHandler("corpus/file_view","pages/corpus/file_view.php",false,["corpus"]);
registerHandler("corpus/csv_get","pages/corpus/csv_get.php",true,["corpus"]);
registerHandler("corpus/file_getdownload","pages/corpus/file_getdownload.php",true,["corpus"]);
registerHandler("corpus/task_getallbycorpus","pages/corpus/task_getallbycorpus.php",true,["corpus"]);
registerHandler("corpus/task_add","pages/corpus/task_add.php",true,["corpus"]);
registerHandler("corpus/archives_get","pages/corpus/archives_get.php",true,["corpus"]);
registerHandler("corpus/data/add","data/corpus/add_file.php",true,["corpus"]);


?>