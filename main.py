def strip_unreal_type_prefixes(source_type_id: str) -> str:
    if source_type_id[0] in {'T', 'U', 'C', 'F', 'E'}:
        return source_type_id[1:]
    else: 
        return source_type_id
    
def opt_param_list(functions: list[str], param_ids: list[str]):
    pass

def gen_bp_img_name(img_label: str) -> str:
    return img_label.lower().replace(' ', '-')

def bp_img(label: str, bp_section: str) -> str:
    #return f'![{label}](img/bp/{bp_section}/{gen_bp_img_name(label)}.png){{ loading=lazy }}'

    #@GUIDANCE: We removed lazy loading for now, this is because the first time you switch between tabs it will abruptly put your scrollbar in an unrelated area. Very annoying! Not worth the performance "gains".
    return f'![{label}](img/bp/{bp_section}/{gen_bp_img_name(label)}.png)'
    
def source_block_base(title, body, header_path):
    return f"""
??? info "Source Location: {title}"
    {body}
    ```c++
    #include "{header_path}"
    ```
"""
def gen_header_path(file_name: str, rel_loc: str|None) -> str:
    result = 'CakeIO/'
    if rel_loc:
        result += f'{rel_loc}/'
    result += f'{file_name}.h'
    return result

def source_loc_single(type_id, rel_loc: str|None = None) -> str:
    header_path = (strip_unreal_type_prefixes(type_id), rel_loc)
    body = f'{type_id} is defined in `{header_path}`'
    return source_block_base(type_id, body, header_path)

def source_loc_custom(id: str, file_name: str, body: str, rel_loc: str|None = None):
    header_path = gen_header_path(file_name, rel_loc)
    return source_block_base(id, body, header_path)

def source_loc_group(group_id, file_name, rel_loc: str|None = None):
    body = f'The following types are all defined in the following header:'
    return source_loc_custom(group_id, file_name, body, rel_loc)

def missing_content(content_id, note=None):
    result = f"""
??? failure "Missing Content: [{content_id}]"
    Content __[{content_id}]__ must be added before the docs are considered complete.
    """
    if note:
        result += f"""

    NOTE: _{note}_
"""
    return result

def define_env(env):
    """
    This is the hook for the variables, macros and filters.
    """
    @env.macro
    def src_loc_group(group_id: str, file_name:str, rel_loc: str|None=None):
        return source_loc_group(group_id, file_name, rel_loc)
    
    @env.macro
    def src_loc_ex(id: str, file_name:str, body: str, rel_loc: str|None=None):
        return source_loc_custom(id, file_name, body, rel_loc)

    @env.macro
    def give_source_loc_single(type_id, rel_loc=None):
        return source_loc_single(type_id, rel_loc)

    @env.macro
    def give_source_loc_single_bp(type_id, rel_loc=None):
        bp_path = f'Blueprint'
        if rel_loc:
            bp_path += f'/{rel_loc}'
        return source_loc_single(type_id, bp_path)
    
    @env.macro
    def mark_missing(content_id, note=None):
        return missing_content(content_id, note)

    @env.macro
    def open_csv_by_typename(typename):
        return f'tables/csvmap_{typename}.csv'

    @env.macro
    def csv_policy(id):
        return open_csv_by_typename(f'ECakePolicy{id}')
    
    @env.macro
    def type_header(type_id, src_fn):
        return f"""{type_id}
{src_fn(type_id)}
"""
    @env.macro
    def bp_img_path(label):
        return bp_img(label, 'path')

    @env.macro
    def bp_img_file_ext(label):
        return bp_img(label, 'file-ext')
    
    @env.macro
    def bp_img_file(label):
        return bp_img(label, 'file')

    @env.macro
    def bp_img_dir(label):
        return bp_img(label, 'dir')
    
    @env.macro
    def bp_file_query_func(label):
        return f"""
    { bp_img_file(label) }
    --8<-- "bp-warn-query-flag.md"
"""
    @env.macro
    def bp_img_error_handling(label):
        return bp_img(label, 'error-handling')

    @env.macro
    def bp_img_cakemix(label):
        return bp_img(label, 'cake-mix-library')

    @env.macro
    def bp_img_async(label):
        return bp_img(label, 'async')

    @env.macro
    def bp_img_ext_filter(label):
        return bp_img(label, 'ext-filter')