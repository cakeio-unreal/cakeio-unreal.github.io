{% capture img_file %}
{{ bp_path}}/{{ bp_file_id }}.png
{% endcapture %}

![](/assets/images/blueprint/{{ img_file | strip }})