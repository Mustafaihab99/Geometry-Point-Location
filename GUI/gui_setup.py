# samy & ashraf 2
import tkinter as tk
from tkinter import ttk
from GeometryFunctions.isConvex import is_convex

class GUISetup:
    def _setup_ui(self):
        """Setup enhanced user interface."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Canvas
        canvas_frame = ttk.LabelFrame(main_frame, text="Visualization Panel", padding=10)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=1100, height=900)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.canvas.bind('<Button-1>', self._on_canvas_click)
        self.canvas.bind('<B1-Motion>', self._on_canvas_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_canvas_release)
        self.canvas.bind('<Motion>', self._on_canvas_hover)
        self.canvas.bind('<Button-3>', self._on_canvas_right_click)  # Right-click to create polygon
        self.canvas.bind('<Double-Button-1>', self._on_canvas_double_click)  # Double-click to edit
        
        # Right panel - Controls with Scrollbar
        control_frame_container = ttk.Frame(main_frame, width=450)
        control_frame_container.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        # Create a canvas with scrollbar for the control panel
        control_canvas = tk.Canvas(control_frame_container, width=450, height=900, highlightthickness=0)
        scrollbar = ttk.Scrollbar(control_frame_container, orient="vertical", command=control_canvas.yview)
        scrollable_frame = ttk.Frame(control_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: control_canvas.configure(scrollregion=control_canvas.bbox("all"))
        )
        
        control_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        control_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        control_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to scroll
        def _on_mousewheel(event):
            control_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        control_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Use scrollable_frame instead of control_frame for all controls
        control_frame = scrollable_frame
        
        # Polygon Management - Compact version
        poly_frame = ttk.LabelFrame(control_frame, text="Polygon Management", padding=5)
        poly_frame.pack(fill=tk.X, pady=(0, 8), padx=2)
        
        # Compact creation controls
        ttk.Label(poly_frame, text="Create:", font=('Arial', 9)).grid(row=0, column=0, sticky=tk.W, padx=2, pady=2)
        
        create_btn_frame = ttk.Frame(poly_frame)
        create_btn_frame.grid(row=0, column=1, columnspan=3, sticky=tk.EW, padx=2, pady=2)
        
        ttk.Button(create_btn_frame, text="New", 
                  command=self._start_new_polygon, width=6).pack(side=tk.LEFT, padx=1)
        ttk.Button(create_btn_frame, text="Finish", 
                  command=self._finish_polygon, width=6).pack(side=tk.LEFT, padx=1)
        ttk.Button(create_btn_frame, text="Cancel", 
                  command=self._cancel_polygon_creation, width=6).pack(side=tk.LEFT, padx=1)
        
        # Compact editing controls
        ttk.Label(poly_frame, text="Edit:", font=('Arial', 9)).grid(row=1, column=0, sticky=tk.W, padx=2, pady=2)
        
        edit_btn_frame = ttk.Frame(poly_frame)
        edit_btn_frame.grid(row=1, column=1, columnspan=3, sticky=tk.EW, padx=2, pady=2)
        
        ttk.Button(edit_btn_frame, text="Start", 
                  command=self._start_editing, width=6).pack(side=tk.LEFT, padx=1)
        ttk.Button(edit_btn_frame, text="Stop", 
                  command=self._stop_editing, width=6).pack(side=tk.LEFT, padx=1)
        ttk.Button(edit_btn_frame, text="Add Vtx", 
                  command=self._add_vertex_to_selected, width=6).pack(side=tk.LEFT, padx=1)
        
        # Quick actions in one line
        ttk.Label(poly_frame, text="Quick:", font=('Arial', 9)).grid(row=2, column=0, sticky=tk.W, padx=2, pady=2)
        
        quick_btn_frame = ttk.Frame(poly_frame)
        quick_btn_frame.grid(row=2, column=1, columnspan=3, sticky=tk.EW, padx=2, pady=2)
        
        ttk.Button(quick_btn_frame, text="Random", 
                  command=self._add_random_polygon, width=8).pack(side=tk.LEFT, padx=1)
        ttk.Button(quick_btn_frame, text="Clear All", 
                  command=self._clear_all_polygons, width=8).pack(side=tk.LEFT, padx=1)
        
        # Current polygons list - compact
        list_frame = ttk.Frame(poly_frame)
        list_frame.grid(row=3, column=0, columnspan=4, sticky=tk.EW, padx=2, pady=5)
        
        ttk.Label(list_frame, text=f"Polygons: {len(self.polygons)}", font=('Arial', 9)).pack(anchor=tk.W)
        self.polygon_listbox = tk.Listbox(list_frame, height=4, font=('Arial', 8))
        self.polygon_listbox.pack(fill=tk.X, pady=2)
        self.polygon_listbox.bind('<<ListboxSelect>>', self._on_polygon_select)
        self._update_polygon_list()
        
        # Compact polygon list buttons
        poly_list_btn_frame = ttk.Frame(poly_frame)
        poly_list_btn_frame.grid(row=4, column=0, columnspan=4, sticky=tk.EW, padx=2, pady=2)
        
        ttk.Button(poly_list_btn_frame, text="Delete", 
                  command=self._delete_selected_polygon, width=8).pack(side=tk.LEFT, padx=1)
        ttk.Button(poly_list_btn_frame, text="Move ↑", 
                  command=lambda: self._reorder_polygon(-1), width=6).pack(side=tk.LEFT, padx=1)
        ttk.Button(poly_list_btn_frame, text="Move ↓", 
                  command=lambda: self._reorder_polygon(1), width=6).pack(side=tk.LEFT, padx=1)
        
        # Compact editing instructions
        edit_info_frame = ttk.LabelFrame(poly_frame, text="Edit Help", padding=3)
        edit_info_frame.grid(row=5, column=0, columnspan=4, sticky=tk.EW, padx=2, pady=5)
        
        info_text = "Dbl-click: Edit\nDrag: Move vertex/edge\nClick edge: Add vertex\nDel: Remove vertex\nDrag center: Move all"
        ttk.Label(edit_info_frame, text=info_text, justify=tk.LEFT, font=('Arial', 8)).pack(anchor=tk.W, padx=2, pady=2)
        
        # Configure grid columns to expand
        for i in range(4):
            poly_frame.columnconfigure(i, weight=1)
        
        # Animation Controls - Compact
        anim_frame = ttk.LabelFrame(control_frame, text="Animation", padding=5)
        anim_frame.pack(fill=tk.X, pady=(0, 8), padx=2)
        
        # Speed control compact
        speed_frame = ttk.Frame(anim_frame)
        speed_frame.pack(fill=tk.X, padx=2, pady=2)
        
        ttk.Label(speed_frame, text="Speed:", font=('Arial', 9)).pack(side=tk.LEFT)
        self.speed_var = tk.IntVar(value=500)
        speed_scale = ttk.Scale(speed_frame, from_=100, to=2000, 
                               variable=self.speed_var, orient=tk.HORIZONTAL,
                               command=lambda v: setattr(self, 'animation_speed', int(float(v))),
                               length=150)
        speed_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Animation buttons in grid
        btn_grid = ttk.Frame(anim_frame)
        btn_grid.pack(fill=tk.X, padx=2, pady=2)
        
        ttk.Button(btn_grid, text="Play", 
                  command=self._play_animation, width=8).grid(row=0, column=0, padx=1, pady=1)
        ttk.Button(btn_grid, text="Step →", 
                  command=self._step_forward, width=8).grid(row=0, column=1, padx=1, pady=1)
        ttk.Button(btn_grid, text="Step ←", 
                  command=self._step_back, width=8).grid(row=1, column=0, padx=1, pady=1)
        ttk.Button(btn_grid, text="Reset", 
                  command=self._reset_animation, width=8).grid(row=1, column=1, padx=1, pady=1)
        
        btn_grid.columnconfigure(0, weight=1)
        btn_grid.columnconfigure(1, weight=1)
        
        # Visualization Options - Compact
        vis_frame = ttk.LabelFrame(control_frame, text="Display", padding=5)
        vis_frame.pack(fill=tk.X, pady=(0, 8), padx=2)
        
        # Options in 2 columns
        options_frame = ttk.Frame(vis_frame)
        options_frame.pack(fill=tk.X, padx=2, pady=2)
        
        self.show_rays_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Rays", 
                       variable=self.show_rays_var, 
                       command=self._draw_dynamic).grid(row=0, column=0, sticky=tk.W, padx=2, pady=1)
        
        self.show_sectors_var = tk.BooleanVar(value=False)  # غيرنا من True ل False
        ttk.Checkbutton(options_frame, text="Sectors", 
                       variable=self.show_sectors_var, 
                       command=self._draw_dynamic).grid(row=0, column=1, sticky=tk.W, padx=2, pady=1)
        
        self.show_center_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Center", 
                       variable=self.show_center_var, 
                       command=self._draw_dynamic).grid(row=1, column=0, sticky=tk.W, padx=2, pady=1)
        
        self.show_animation_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Animation", 
                       variable=self.show_animation_var, 
                       command=self._draw_dynamic).grid(row=1, column=1, sticky=tk.W, padx=2, pady=1)
        
        self.show_search_range_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Search Range", 
                       variable=self.show_search_range_var, 
                       command=self._draw_dynamic).grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=2, pady=1)
        
        self.highlight_editing_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Highlight Edit", 
                       variable=self.highlight_editing_var, 
                       command=self._draw_static).grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=2, pady=1)
        
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        
        # Test Points - Compact
        test_frame = ttk.LabelFrame(control_frame, text="Test Points", padding=5)
        test_frame.pack(fill=tk.X, pady=(0, 8), padx=2)
        
        # Instructions compact
        instr_text = "Left: Test/Move\nRight: Add vertices\nDbl-click: Edit polygon"
        ttk.Label(test_frame, text=instr_text, justify=tk.LEFT, font=('Arial', 8)).pack(anchor=tk.W, padx=2, pady=2)
        
        # Test point buttons
        test_btn_frame = ttk.Frame(test_frame)
        test_btn_frame.pack(fill=tk.X, padx=2, pady=2)
        
        ttk.Button(test_btn_frame, text="Clear Points", 
                  command=self._clear_test_points, width=12).pack(side=tk.LEFT, padx=1)
        ttk.Button(test_btn_frame, text="Random Point", 
                  command=self._add_random_point, width=12).pack(side=tk.LEFT, padx=1)
        
        # Algorithm Information - Compact but scrollable
        info_frame = ttk.LabelFrame(control_frame, text="Algorithm Info", padding=5)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8), padx=2)
        
        # Create a text widget with scrollbar inside info_frame
        info_container = ttk.Frame(info_frame)
        info_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.info_text = tk.Text(info_container, height=12, width=40, wrap=tk.WORD, font=('Arial', 9))
        info_scrollbar = ttk.Scrollbar(info_container, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Statistics - Compact but scrollable
        stats_frame = ttk.LabelFrame(control_frame, text="Statistics", padding=5)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8), padx=2)
        
        # Create a text widget with scrollbar inside stats_frame
        stats_container = ttk.Frame(stats_frame)
        stats_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.stats_text = tk.Text(stats_container, height=10, width=40, wrap=tk.WORD, font=('Arial', 9))
        stats_scrollbar = ttk.Scrollbar(stats_container, command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_scrollbar.set)
        
        self.stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stats_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Actions - Compact
        action_frame = ttk.LabelFrame(control_frame, text="Actions", padding=5)
        action_frame.pack(fill=tk.X, pady=(0, 8), padx=2)
        
        action_btn_frame = ttk.Frame(action_frame)
        action_btn_frame.pack(fill=tk.X, padx=2, pady=2)
        
        ttk.Button(action_btn_frame, text="Example 1", 
                  command=lambda: self._load_example(1), width=10).pack(side=tk.LEFT, padx=1)
        ttk.Button(action_btn_frame, text="Example 2", 
                  command=lambda: self._load_example(2), width=10).pack(side=tk.LEFT, padx=1)
        ttk.Button(action_btn_frame, text="Reset View", 
                  command=self._reset_view, width=10).pack(side=tk.LEFT, padx=1)
        
        # Bind keyboard shortcuts
        self.root.bind('<Delete>', self._delete_selected_vertex)
        self.root.bind('<Escape>', self._stop_editing)
        self.root.bind('<Control-z>', self._undo_last_change)
        
        self._update_info()
        self._update_stats()