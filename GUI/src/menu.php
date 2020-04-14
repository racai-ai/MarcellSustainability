<?php


$PLATFORM=[
  "path"=>"home/home",   // this is the main page
  "menu"=>[

      [
        "label"=>"Home",
        "icon"=>"c-deep-purple-500 ti-comment-alt",
        "path"=>"home/home",
        "menu"=>[
            ["label"=>"Introduction", "path"=>"home/home"],
        ]
      ],


      [
        "label"=>"Corpora",
        "icon"=>"c-deep-purple-500 ti-comment-alt",
        "rights"=>["corpus"],
        "menu"=>[
            ["label"=>"List", "path"=>"corpus/list","rights"=>["corpus"]],
        ]
      ],
      
  ]    
];


?>