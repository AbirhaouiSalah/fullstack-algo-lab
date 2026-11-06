#!/usr/bin/env python3
"""Idempotent LAB-103 scaffold generator. Run from repository root."""
import argparse
import json
import re
from pathlib import Path

CATALOG = {
 'binary-search': [
 ('Binary Search','Easy','binary-search'),('Search a 2D Matrix','Medium','search-2d-matrix'),('Koko Eating Bananas','Medium','eating-bananas'),('Find Minimum In Rotated Sorted Array','Medium','find-minimum-in-rotated-sorted-array'),('Search In Rotated Sorted Array','Medium','find-target-in-rotated-sorted-array'),('Time Based Key Value Store','Medium','time-based-key-value-store'),('Median of Two Sorted Arrays','Hard','median-of-two-sorted-arrays')],
 'sliding-window': [
 ('Best Time to Buy And Sell Stock','Easy','buy-and-sell-crypto'),('Longest Substring Without Repeating Characters','Medium','longest-substring-without-duplicates'),('Longest Repeating Character Replacement','Medium','longest-repeating-substring-with-replacement'),('Permutation In String','Medium','permutation-string'),('Minimum Window Substring','Hard','minimum-window-with-characters'),('Sliding Window Maximum','Hard','sliding-window-maximum')],
 'linked-list': [
 ('Reverse Linked List','Easy',None),('Merge Two Sorted Lists','Easy',None),('Linked List Cycle','Easy',None),('Reorder List','Medium',None),('Remove Nth Node From End of List','Medium',None),('Copy List With Random Pointer','Medium',None),('Add Two Numbers','Medium',None),('Find The Duplicate Number','Medium',None),('LRU Cache','Medium',None),('Merge K Sorted Lists','Hard',None),('Reverse Nodes In K Group','Hard',None)],
 'trees': [
 ('Invert Binary Tree','Easy',None),('Maximum Depth of Binary Tree','Easy',None),('Diameter of Binary Tree','Easy',None),('Balanced Binary Tree','Easy',None),('Same Tree','Easy',None),('Subtree of Another Tree','Easy',None),('Lowest Common Ancestor of a Binary Search Tree','Medium',None),('Binary Tree Level Order Traversal','Medium',None),('Binary Tree Right Side View','Medium',None),('Count Good Nodes In Binary Tree','Medium',None),('Validate Binary Search Tree','Medium',None),('Kth Smallest Element In a Bst','Medium',None),('Construct Binary Tree From Preorder And Inorder Traversal','Medium',None),('Binary Tree Maximum Path Sum','Hard',None),('Serialize And Deserialize Binary Tree','Hard',None)]
}
PREREQS = {
 'binary-search': [('Search Array','https://neetcode.io/courses/dsa-for-beginners/14'),('Search Range','https://neetcode.io/courses/dsa-for-beginners/15')],
 'sliding-window': [('Sliding Window Fixed Size','https://neetcode.io/courses/advanced-algorithms/1'),('Sliding Window Variable Size','https://neetcode.io/courses/advanced-algorithms/2')],
 'linked-list': [('Singly Linked Lists',None),('Doubly Linked Lists',None),('Fast and Slow Pointers',None)],
 'trees': [('BST Insert and Remove',None),('Depth-First Search',None),('Breadth-First Search',None),('BST Sets and Maps',None),('Iterative DFS',None)]
}

def slugify(name):
    return re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,default=Path.cwd(),help='Existing repository root')
    args=ap.parse_args()
    root=args.root.resolve()
    if not (root/'algorithms').is_dir():
        ap.error(f'No algorithms/ directory at {root}; pass --root pointing to your repository')
    created=0; skipped=0
    records=[]
    for category, problems in CATALOG.items():
        index=[f'# {category.replace("-"," ").title()} — LAB-103','',f'**Problems:** {len(problems)}','', '## Prerequisites','']
        for label,url in PREREQS[category]:
            index.append(f'- [{label}]({url})' if url else f'- {label} (course reference; URL not supplied)')
        index += ['', '| # | Problem | Difficulty | Status |', '|---:|---|---|---|']
        for i,(name,difficulty,neetcode_slug) in enumerate(problems,1):
            slug=slugify(name)
            directory=root/'algorithms'/category/slug
            directory.mkdir(parents=True,exist_ok=True)
            url=f'https://neetcode.io/problems/{neetcode_slug}/question?list=neetcode150' if neetcode_slug else None
            index.append(f'| {i} | [{name}]({url}) | {difficulty} | Not started |' if url else f'| {i} | {name} | {difficulty} | Not started |')
            readme=f'''# {name}\n\n- **LAB:** LAB-103\n- **Theme:** {category}\n- **Difficulty:** {difficulty}\n- **Status:** Not started\n- **Official source:** {url or 'NeetCode Roadmap — https://neetcode.io/roadmap (exact problem URL not provided)'}\n\n## Problem statement\n\nOpen the official NeetCode problem and reformulate its statement here in your own words.\n\n## Inputs, outputs and constraints\n\n- Inputs: TODO\n- Outputs: TODO\n- Constraints: TODO (verify against official statement)\n\n## Examples and edge cases\n\n- Typical case: TODO\n- Boundary case: TODO\n- Invalid or empty case (if applicable): TODO\n\n## Reasoning journal\n\n1. Brute-force idea: TODO\n2. Invariant / key observation: TODO\n3. Chosen data structure: TODO\n4. Dry run: TODO\n5. Optimized approach: TODO\n\n## Verification\n\n- [ ] Problem understood\n- [ ] Python solution implemented\n- [ ] TypeScript solution implemented\n- [ ] Python tests passing\n- [ ] TypeScript tests passing\n- [ ] Complexity documented\n- [ ] Can explain without notes\n'''
            templates={
                'README.md':readme,
                'solution.py':f'"""{name} — implement after solving the problem.\n\nDefine the signature from the official statement before writing the algorithm.\n"""\n',
                'test_solution.py':f'"""Tests for {name}. Add concrete assertions after confirming the API.\n\nUse pytest; avoid treating an empty suite as a passed exercise.\n"""\n',
                'solution.ts':f'/** {name}. Implement after deriving the solution.\n * Define the function signature from the official problem statement.\n */\nexport {{}};\n',
                'solution.test.ts':f'import {{ describe, it }} from "vitest";\n\ndescribe("{name}", () => {{\n  it.todo("handles the official example");\n  it.todo("handles edge cases");\n}});\n',
                'complexity.md':f'# Complexity — {name}\n\n## Brute force\n\n- Time: TODO\n- Space: TODO\n\n## Optimized approach\n\n- Time: TODO\n- Space: TODO\n\n## Justification\n\nExplain the number of iterations, data structure operations and auxiliary memory.\n',
            }
            for filename,content in templates.items():
                file=directory/filename
                if file.exists(): skipped+=1
                else: file.write_text(content,encoding='utf-8');created+=1
            records.append({'category':category,'name':name,'slug':slug,'difficulty':difficulty,'url':url,'status':'not_started'})
        index_path=root/'algorithms'/category/'LAB103_INDEX.md'
        if not index_path.exists():index_path.write_text('\n'.join(index)+'\n',encoding='utf-8');created+=1
        else:skipped+=1
    docs=root/'docs'/'algorithms'
    docs.mkdir(parents=True,exist_ok=True)
    catalog_path=docs/'lab103-catalog.json'
    if not catalog_path.exists():catalog_path.write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');created+=1
    else:skipped+=1
    print(f'LAB-103: {len(records)} problems; {created} files created; {skipped} existing files preserved')
    print('NOTE: TODO tests and placeholder solutions do not indicate mastery.')

if __name__=='__main__':main()
