import sys
import json


def range_is_valid(g_start, g_end, g_name, groups):
    for g in groups:
        if (g_start >= g[0] and g_start < g[1]) or (g_end > g[0] and g_end < g[1]):
            raise Exception(f"Error: intersecting ranges: {g_name} and {g[2]}")
    return True


def module_get_inputs(module):
    inputs = module['inputs']
    i_size = 0
    i_groups = []
    i_ranges = []
    offset = 0
    for g in inputs:
        g_name = g['name']
        g_start = g['range'][0]
        g_end = g['range'][1]
        g_size = g_end - g_start
        i_size += g_size
        if range_is_valid(g_start, g_end, g_name, i_groups):
            i_groups.append([g_start, g_end, g_name])
            i_ranges.append({'name': g_name, 'offset': offset, 'size': g_size, 'range': [g_start, g_end]})
        offset += g_size
    return {
        'size': i_size,
        'offset': 0,
        'range': [0, i_size],
        'groups': i_ranges
    }


def module_get_groups(groups, offset):
    cluster = {
        'size': 0,
        'offset': offset,
        'range': [offset],
        'groups': []
    }
    for group in groups:
        g_range = [cluster['size'], cluster['size'] + group['size']]
        cluster['groups'].append({
            'name': group['name'],
            'size': group['size'],
            'offset': offset,
            'range': g_range,
            'type': group['type'],
            'inputs': group['inputs']
        })
        cluster['size'] += group['size']
        offset += group['size']
    cluster['range'].append(offset)
    return cluster
