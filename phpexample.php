<!DOCTYPE html>
<html>
<body>

<code>
<?php
   $str = "$htmlstring = '<html><head> </head><body></a>Washington, DC 20500<br/>202-456-1111</a></body></html>'";
echo htmlspecialchars($str);
?><br>
   $soup = BeautifulSoup(html, 'lxml')<br>
   $soup.get_text()<br>
   :'Washington, DC 20500202-456-1111'

</code>



</body>
</html>
