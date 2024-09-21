{% capture img_file %}
{{ bp_path}}/{{ bp_file_id }}.gif
{% endcapture %}

![](/assets/images/blueprint/{{ img_file | strip }})