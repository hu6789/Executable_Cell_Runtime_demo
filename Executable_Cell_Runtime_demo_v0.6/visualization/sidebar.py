# visualization/sidebar.py

"""
Visualization Sidebar

Right inspection panel for MacroImmunet Viewer.

Shows

    - basic information
    - important nodes
    - active behaviors
    - labels

Everything comes from visualization snapshot.
"""

import pygame


# ==========================================================
# Sidebar
# ==========================================================

class Sidebar:

    def __init__(

        self,

        rect=(1100, 40, 320, 820)

    ):

        self.rect = pygame.Rect(*rect)

        pygame.font.init()

        self.title_font = pygame.font.SysFont(
            "Arial",
            24,
            bold=True
        )

        self.header_font = pygame.font.SysFont(
            "Arial",
            18,
            bold=True
        )

        self.font = pygame.font.SysFont(
            "Arial",
            16
        )

    # ======================================================
    # Render
    # ======================================================

    def render(
        self,
        screen,
        snapshot,
        selected_object
    ):

        pygame.draw.rect(
            screen,
            (42,42,48),
            self.rect
        )

        pygame.draw.rect(
            screen,
            (90,90,90),
            self.rect,
            1
        )
        
        inspectors = snapshot.get(
            "inspectors",
            {}
        )

        if not selected_object:

            text = self.title_font.render(
                "Select an Object",
                True,
                (220,220,220)
            )

            screen.blit(
                text,
                (
                    self.rect.left+20,
                    self.rect.top+20
                )
            )

            return

        if not isinstance(selected_object,list):

            selected_object=[
                selected_object
            ]
   

        y=self.rect.top+20


        # ================================
        # draw all selected objects
        # ================================

        for obj in selected_object:


            object_type=obj.get(
                "object_type"
            )
 
            data=obj.get(
                "data",
                {}
            )
            
            inspector = None


            if object_type=="cell":

                cell_id=data.get(
                    "id"
                )

                inspector = inspectors.get(
                    cell_id
                )
                
                print(
                    "INSPECTOR:",
                    inspector
                )

            if object_type=="cell":

                y=self.render_cell(
                    screen,
                    data,
                    y,
                    inspector
                )

            elif object_type=="field":

                y=self.render_field(
                   screen,
                   data,
                   y
                )


            y+=20

    # ======================================================
    # Helpers
    # ======================================================

    def runtime(

        self,

        obj

    ):

        if not obj:

            return {}

        # inspector snapshot
        if "behaviors" in obj:

            return obj

        # old runtime object
        return obj.get(
            "runtime_state",
            {}
        )

    def header(

        self,

        screen,

        title,

        y

    ):

        surf = self.header_font.render(

            title,

            True,

            (120,210,255)

        )

        screen.blit(

            surf,

            (

                self.rect.left+18,

                y

            )

        )

        return y+28

    def text(

        self,

        screen,

        string,

        y,

        color=(220,220,220)

    ):

        surf = self.font.render(

            str(string),

            True,

            color

        )

        screen.blit(

            surf,

            (

                self.rect.left+20,

                y

            )

        )

    # ======================================================
    # Title
    # ======================================================

    def draw_title(

        self,

        screen,

        obj,

        y

    ):

        title = obj.get(

            "type",

            "Cell"

        )

        surf = self.title_font.render(

            title,

            True,

            (255,255,255)

        )

        screen.blit(

            surf,

            (

                self.rect.left+20,

                y

            )

        )

        return y+42

    # ======================================================
    # Basic
    # ======================================================

    def draw_basic(

        self,

        screen,

        obj,

        y

    ):

        y = self.header(

            screen,

            "Information",

            y

        )

        self.text(

            screen,

            f"ID : {obj.get('id')}",

            y

        )

        y += 22

        self.text(

            screen,

            f"Alive : {obj.get('alive')}",

            y

        )

        y += 22

        self.text(

            screen,

            f"Position : {obj.get('position')}",

            y

        )

        return y+34

    # ======================================================
    # Field Info
    # ======================================================

    def draw_field_info(
        self,
        screen,
        obj,
        y
    ):

        title = obj.get(
            "field_type",
            "Field"
        )


        surf = self.title_font.render(
            title,
            True,
            (255,255,255)
        )

        screen.blit(
            surf,
            (
                self.rect.left+20,
                y
            )
        )


        y += 45


        self.text(
            screen,
            "Field Information",
            y
        )

        y += 25


        self.text(
            screen,
            f"Position : {obj.get('position')}",
            y
        )

        y += 22


        self.text(
            screen,
            f"Strength : {obj.get('strength'):.3f}",
            y
        )

    # ======================================================
    # Nodes
    # ======================================================

    def important_nodes(

        self,

        cell_type

    ):

        mapping = {

            "host_cell":[

                "ATP",

                "pMHC",

                "cell_membrane",

                "influenza",

                "pathogen_signal"

            ],

            "cd4_t_cell":[

                "ATP",

                "TCR",

                "IL2R",

                "IL2",

                "amino_acid"

            ],

            "cd8_t_cell":[

                "ATP",

                "TCR",

                "IL2R",

                "perforin",

                "amino_acid"

            ]

        }

        return mapping.get(

            cell_type,

            []

        )

    def draw_nodes(

        self,

        screen,

        obj,

        y

    ):

        y = self.header(

            screen,

            "Nodes",

            y

        )

        runtime = self.runtime(

            obj

        )

        nodes = runtime.get(

            "nodes",

            {}

        )

        wanted = self.important_nodes(

            obj.get(

                "type"

            )

        )

        if not wanted:

            self.text(

                screen,

                "(none)",

                y

            )

            return y+30

        for name in wanted:

            value = nodes.get(

                name,

                "-"

            )

            self.text(

                screen,

                f"{name:18} {value}",

                y

            )

            y += 20

        return y+18

    # ======================================================
    # Behaviors
    # ======================================================

    def draw_behaviors(

        self,

        screen,

        obj,

        y

    ):

        y = self.header(

            screen,

            "Behaviors",

            y

        )

        runtime = self.runtime(

            obj

        )

        behaviors = runtime.get(

            "behaviors",

            {}

        )
        
        print(
            "SIDEBAR BEHAVIORS:",
            behaviors
        )

        if isinstance(
            behaviors,
            list
        ):

            entries = []

            for item in behaviors:

                if isinstance(item,dict):

                    entries.append(
                        (
                            item.get("name","unknown"),
                            item.get("strength",0)
                        )
                    )

                else:

                    entries.append(
                        (
                            str(item),
                            None
                        )
                    )

        else:

            entries = [
                (name,None)
                for name in behaviors
            ]


        if not entries:

            self.text(
                screen,
                "(none)",
                y
            )

            return y+28


        for name,strength in entries:

            if strength is not None:

                text = (
                    f"{name}"
                    f"  {strength:.6f}"
                )

            else:

                text=name


            self.text(
                screen,
                text,
                y
            )

            y += 20

        return y+18

    def build_base_behaviors(self, package):

        output=[]

        for item in package.get(
            "base_behaviors",
            []
        ):

            if isinstance(item,dict):

                output.append(
                    item.get("name")
                )

            else:

                output.append(item)

        return output
    
    # ======================================================
    # Labels
    # ======================================================

    def draw_labels(

        self,

        screen,

        obj,

        y

    ):

        y = self.header(

            screen,

            "Labels",

            y

        )

        runtime = self.runtime(

            obj

        )

        labels = runtime.get(

            "labels",

            []

        )

        if not labels:

            self.text(

                screen,

                "(none)",

                y

            )

            return

        for label in labels:

            surf = self.font.render(

                f"[ {label} ]",

                True,

                (255,220,120)

            )

            screen.blit(

                surf,

                (

                    self.rect.left+20,

                    y

                )

            )

            y += 22

    def render_field(
        self,
        screen,
        field,
        y
    ):

        self.text(
            screen,
            "FIELD",
            y
        )

        y+=25

        self.text(
            screen,
            f"Type:{field.get('field_type')}",
            y
        )

        y+=22

        self.text(
            screen,
            f"Position:{field.get('position')}",
            y
        )

        y+=22

        self.text(
            screen,
            f"Strength:{field.get('strength')}",
            y
        )

        return y
        
    def render_cell(
        self,
        screen,
        cell,
        y,
        inspector
    ):

        self.text(
            screen,
            "CELL",
            y
        ) 

        y+=25

        self.text(
            screen,
            f"ID:{cell.get('id')}",
            y
        )

        y+=22

        self.text(
            screen,
            f"Type:{cell.get('type')}",
            y
        )

        y+=22

        self.text(
            screen,
            f"Position:{cell.get('position')}",
            y
        )
        
        y+=30

        self.text(
            screen,
            "Nodes",
            y
        )

        y+=22


        for node in inspector.get(
            "nodes",
            []
        ):

            self.text(
                screen,
                f"{node['name']} : {node['value']}",
                y
            )

            y+=20
        
        y+=20

        self.text(
            screen,
            "Behaviors",
            y
        )

        y+=22


        for behavior in inspector.get(
            "behaviors",
            []
        ):

            name = behavior.get(
                "name",
                "unknown"
            )

            strength = behavior.get(
                "strength",
                0
            )

            self.text(
                screen,
                f"{name} : {strength:.3e}",
                y
            )

            y += 20

        return y
