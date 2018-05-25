<!DOCTYPE html>
<html lang="en">
  <head>
  </head>
  <body >
<div>
  <p >Type a website url into the box below.</p>
    <form method='POST', action="/">
        <div class='form-group'>
            <input type="text" name="website">
        </div>
        <input class="btn btn-primary" type="submit" value="submit">
    </form>

<table>
{%- if website -%}
        <th> url: </th>
        <td> {{ website }} </td>
{% endif %}
{% for key, value in information.items() %}
{%- if value -%}
   <tr>
        <th> {{ key }} </th>
        <td> {{ value }} </td>
   </tr>
{% endif %}
{% endfor %}
</table>

          </div>

  </body>

</html>
