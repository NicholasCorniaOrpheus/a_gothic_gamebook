"""
Markdown pages generation
"""

import snakemd


def generate_scenes_md(
    agg_dict, agg_scenes_markdown_directory, base_url, file_mark=" - AGG 2025"
):
    # initialize new Markdown document
    for scene in agg_dict["scenes"]:
        doc = snakemd.Document()
        # add YAML metadata
        doc.add_raw(
            f"""---
hide:\n 
- title\n
- toc\n
search:\n
 boost: 2\n
title: {scene["title"][0]}\n
tags: {",".join(scene["keyword"])}\n 
---

"""
        )

        # Add title
        doc.add_heading(scene["title"][0], 1)

        # Add description
        doc.add_heading("Description", 2)
        doc.add_paragraph("_" + scene["description"][0].strip() + "_")
        doc.add_horizontal_rule()
        # Add comes_from
        doc.add_heading("Comes from", 2)
        for parent in scene["comes_from"]:
            doc.add_paragraph(
                str(
                    snakemd.Inline(parent.replace(file_mark, "")).link(
                        base_url + "/scenes/" + parent.replace(" ", "_") + ".md"
                    )
                )
            )
        doc.add_horizontal_rule()
        # Add goes_to plus questions
        if scene["goes_to_A"][0] != "":
            doc.add_heading("Choices", 2)
            table_header = ["Option", "Question", "Goes to"]
            table_align = [
                snakemd.Table.Align.CENTER,
                snakemd.Table.Align.LEFT,
                snakemd.Table.Align.LEFT,
            ]
            table_rows = []
            table_rows.append(
                [
                    "A",
                    scene["question_A"][0],
                    str(
                        snakemd.Inline(
                            scene["goes_to_A"][0].replace(file_mark, "")
                        ).link(
                            base_url
                            + "/scenes/"
                            + scene["goes_to_A"][0].replace(" ", "_")
                            + ".md"
                        )
                    ),
                ]
            )
            if scene["goes_to_B"][0] != "":
                table_rows.append(
                    [
                        "B",
                        scene["question_B"][0],
                        str(
                            snakemd.Inline(
                                scene["goes_to_B"][0].replace(file_mark, "")
                            ).link(
                                base_url
                                + "/scenes/"
                                + scene["goes_to_B"][0].replace(" ", "_")
                                + ".md"
                            )
                        ),
                    ]
                )
                if scene["goes_to_C"][0] != "":
                    table_rows.append(
                        [
                            "C",
                            scene["question_B"][0],
                            str(
                                snakemd.Inline(
                                    scene["goes_to_C"][0].replace(file_mark, "")
                                ).link(
                                    base_url
                                    + "/scenes/"
                                    + scene["goes_to_C"][0].replace(" ", "_")
                                    + ".md"
                                )
                            ),
                        ]
                    )

            doc.add_table(table_header, table_rows, align=table_align)
            doc.add_horizontal_rule()

        # Add musical pieces
        doc.add_heading("Songs", 2)
        for song in scene["music"]:
            doc.add_paragraph(
                str(
                    snakemd.Inline(song).link(
                        base_url + "/songs/" + song.replace(" ", "_") + ".md"
                    )
                )
            )
        doc.add_horizontal_rule()

        # save .md file
        html_title = scene["label"][0].replace(" ", "_")
        doc.dump(html_title, directory=agg_scenes_markdown_directory)
