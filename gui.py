import tkinter as tk
from tkinter import ttk, messagebox
import database
from content_based import recommend_content
from collaborative import recommend_collab

# Refined Theme Colors
BG_COLOR = "#12121e"          # Darker background
FG_COLOR = "#ffffff"          # White text
ACCENT_COLOR = "#7b61ff"      # Vibrant purple
SECONDARY_BG = "#1f1f33"      # Lighter surface color
HIGHLIGHT_COLOR = "#9d88ff"   # Hover/Highlight purple
TEXT_COLOR = "#b3b3b3"        # Subtitle/Secondary text color
SUCCESS_COLOR = "#00e676"     # Green for match scores
WARN_COLOR = "#ffea00"        # Yellow for ratings

class EarningApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI E-Learning Recommendation System")
        self.geometry("1000x700")
        self.configure(bg=BG_COLOR)
        self.minsize(800, 600)
        
        self.current_user_id = None
        self.current_user_name = None

        self.style = ttk.Style(self)
        self.setup_styles()

        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        
        self.create_login_frame()
        self.show_frame("LoginFrame")

    def setup_styles(self):
        self.style.theme_use("clam")
        
        # General Elements
        self.style.configure("TFrame", background=BG_COLOR)
        self.style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=("Segoe UI", 12))
        
        # Headers
        self.style.configure("Header.TLabel", font=("Segoe UI", 28, "bold"), foreground=ACCENT_COLOR, background=BG_COLOR)
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 16), foreground=TEXT_COLOR, background=BG_COLOR)
        
        # Primary Buttons
        self.style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), background=ACCENT_COLOR, foreground=FG_COLOR, borderwidth=0, padding=10)
        self.style.map("Primary.TButton", background=[("active", HIGHLIGHT_COLOR)])
        
        # Sidebar
        self.style.configure("Sidebar.TFrame", background=SECONDARY_BG)
        self.style.configure("Sidebar.TButton", font=("Segoe UI", 12), background=SECONDARY_BG, foreground=FG_COLOR, borderwidth=0, padding=12, anchor="w")
        self.style.map("Sidebar.TButton", background=[("active", HIGHLIGHT_COLOR)], foreground=[("active", "#ffffff")])
        
        # Cards
        self.style.configure("Card.TFrame", background=SECONDARY_BG, relief="flat")
        self.style.configure("CardTitle.TLabel", background=SECONDARY_BG, foreground=FG_COLOR, font=("Segoe UI", 16, "bold"))
        self.style.configure("CardText.TLabel", background=SECONDARY_BG, foreground=TEXT_COLOR, font=("Segoe UI", 11))
        self.style.configure("CardHighlight.TLabel", background=SECONDARY_BG, foreground=SUCCESS_COLOR, font=("Segoe UI", 12, "bold"))
        
        # Input Fields
        self.style.configure("TEntry", fieldbackground=SECONDARY_BG, foreground=FG_COLOR, borderwidth=0, padding=8)
        self.style.configure("TCombobox", fieldbackground=SECONDARY_BG, background=SECONDARY_BG, foreground=FG_COLOR, arrowcolor=FG_COLOR, padding=8)
        
        # Treeview (Tables)
        self.style.configure("Treeview", background=SECONDARY_BG, fieldbackground=SECONDARY_BG, foreground=FG_COLOR, rowheight=35, font=("Segoe UI", 11), borderwidth=0)
        self.style.map("Treeview", background=[("selected", ACCENT_COLOR)], foreground=[("selected", FG_COLOR)])
        self.style.configure("Treeview.Heading", background=ACCENT_COLOR, foreground=FG_COLOR, font=("Segoe UI", 12, "bold"), padding=5, borderwidth=0)
        
        # Notebook (Tabs)
        self.style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=SECONDARY_BG, foreground=FG_COLOR, padding=[20, 10], font=("Segoe UI", 12, "bold"), borderwidth=0)
        self.style.map("TNotebook.Tab", background=[("selected", ACCENT_COLOR)], foreground=[("selected", FG_COLOR)])

    def create_login_frame(self):
        frame = ttk.Frame(self.container)
        self.frames["LoginFrame"] = frame
        frame.place(relwidth=1, relheight=1)

        # Center card for login
        center_frame = tk.Frame(frame, bg=SECONDARY_BG, padx=40, pady=40, bd=0)
        center_frame.place(relx=0.5, rely=0.5, anchor="center", width=500)

        # Title
        tk.Label(center_frame, text="AI Learn", font=("Segoe UI", 32, "bold"), fg=ACCENT_COLOR, bg=SECONDARY_BG).pack(pady=(0, 5))
        tk.Label(center_frame, text="Smarter course recommendations", font=("Segoe UI", 12), fg=TEXT_COLOR, bg=SECONDARY_BG).pack(pady=(0, 30))

        # Login Section
        tk.Label(center_frame, text="Returning User?", font=("Segoe UI", 11, "bold"), fg=FG_COLOR, bg=SECONDARY_BG).pack(anchor="w", pady=(0, 5))
        self.user_var = tk.StringVar()
        self.user_dropdown = ttk.Combobox(center_frame, textvariable=self.user_var, state="readonly", font=("Segoe UI", 12))
        self.update_user_dropdown()
        self.user_dropdown.pack(fill="x", pady=(0, 10), ipady=5)
        ttk.Button(center_frame, text="Log In", style="Primary.TButton", command=self.login).pack(fill="x", pady=(0, 25))

        # Divider
        tk.Frame(center_frame, height=1, bg=TEXT_COLOR).pack(fill="x", pady=10)

        # Register Section
        tk.Label(center_frame, text="New User Registration", font=("Segoe UI", 11, "bold"), fg=FG_COLOR, bg=SECONDARY_BG).pack(anchor="w", pady=(15, 5))
        
        self.new_name_var = tk.StringVar()
        ttk.Entry(center_frame, textvariable=self.new_name_var, font=("Segoe UI", 12)).pack(fill="x", pady=(0, 10), ipady=5)
        # Placeholder logic for Entry
        self.new_name_var.set("Enter your name")
        
        self.new_interest_var = tk.StringVar()
        ttk.Entry(center_frame, textvariable=self.new_interest_var, font=("Segoe UI", 12)).pack(fill="x", pady=(0, 15), ipady=5)
        self.new_interest_var.set("Main interest (e.g., Python)")
        
        ttk.Button(center_frame, text="Create Account", style="Primary.TButton", command=self.register).pack(fill="x", pady=(0, 10))

    def update_user_dropdown(self):
        users = database.get_all_users()
        if users:
            self.user_dropdown["values"] = [f"{u[0]} - {u[1]}" for u in users]
            self.user_dropdown.current(0)
        else:
            self.user_dropdown["values"] = ["No users available"]

    def login(self):
        selection = self.user_var.get()
        if not selection or selection == "No users available":
            messagebox.showerror("Error", "Please select a valid user.")
            return
        
        user_id = int(selection.split(" - ")[0])
        user = database.get_user(user_id)
        if user:
            self.current_user_id = user[0]
            self.current_user_name = user[1]
            self.create_dashboard()
            self.show_frame("DashboardFrame")

    def register(self):
        name = self.new_name_var.get().strip()
        interest = self.new_interest_var.get().strip()
        
        if not name or not interest or name == "Enter your name" or interest == "Main interest (e.g., Python)":
            messagebox.showerror("Error", "Please fill in both name and valid interest.")
            return
            
        user_id = database.add_user(name, interest)
        self.current_user_id = user_id
        self.current_user_name = name
        self.create_dashboard()
        self.show_frame("DashboardFrame")

    def create_dashboard(self):
        if "DashboardFrame" in self.frames:
            self.frames["DashboardFrame"].destroy()
            
        frame = ttk.Frame(self.container)
        self.frames["DashboardFrame"] = frame
        frame.place(relwidth=1, relheight=1)

        # Sidebar
        sidebar = ttk.Frame(frame, style="Sidebar.TFrame", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # User Profile Header in Sidebar
        profile_frame = tk.Frame(sidebar, bg=SECONDARY_BG, pady=30)
        profile_frame.pack(fill="x")
        
        # Simulated Avatar
        avatar_canvas = tk.Canvas(profile_frame, width=60, height=60, bg=SECONDARY_BG, highlightthickness=0)
        avatar_canvas.pack(pady=(0, 10))
        avatar_canvas.create_oval(5, 5, 55, 55, fill=ACCENT_COLOR, outline="")
        avatar_canvas.create_text(30, 30, text=self.current_user_name[0].upper(), font=("Segoe UI", 24, "bold"), fill=FG_COLOR)
        
        tk.Label(profile_frame, text=self.current_user_name, font=("Segoe UI", 16, "bold"), fg=FG_COLOR, bg=SECONDARY_BG).pack()
        tk.Label(profile_frame, text="Student", font=("Segoe UI", 10), fg=TEXT_COLOR, bg=SECONDARY_BG).pack()

        # Navigation Buttons
        nav_buttons = [
            ("📚  Browse Courses", self.show_browse_frame),
            ("⭐  Rate Courses", self.show_rate_frame),
            ("🎯  Recommendations", self.show_recommendations_frame),
            ("📊  My Ratings", self.show_my_ratings_frame),
        ]

        for text, command in nav_buttons:
            ttk.Button(sidebar, text=text, command=command, style="Sidebar.TButton").pack(fill="x", pady=2, padx=10)

        # Logout at the bottom
        ttk.Frame(sidebar, style="Sidebar.TFrame").pack(fill="both", expand=True) # Spacer
        ttk.Button(sidebar, text="🚪  Logout", command=self.logout, style="Sidebar.TButton").pack(fill="x", pady=20, padx=10, side="bottom")

        # Main Content Area
        self.content_area = ttk.Frame(frame)
        self.content_area.pack(side="right", fill="both", expand=True)
        
        self.content_frames = {}
        self.create_browse_frame()
        self.create_rate_frame()
        self.create_recommendations_frame()
        self.create_my_ratings_frame()
        
        self.show_browse_frame()

    def show_content_frame(self, frame_name):
        for frame in self.content_frames.values():
            frame.place_forget()
        self.content_frames[frame_name].place(relwidth=1, relheight=1)

    def create_header(self, parent, title, subtitle):
        header_frame = tk.Frame(parent, bg=BG_COLOR)
        header_frame.pack(fill="x", padx=40, pady=(40, 20))
        ttk.Label(header_frame, text=title, style="Header.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text=subtitle, style="SubHeader.TLabel").pack(anchor="w")
        return header_frame

    def create_browse_frame(self):
        frame = ttk.Frame(self.content_area)
        self.content_frames["Browse"] = frame
        
        self.create_header(frame, "Browse Courses", "Explore our library of 50+ premium tech courses.")
        
        # Search Frame
        search_frame = tk.Frame(frame, bg=SECONDARY_BG, padx=20, pady=15)
        search_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        tk.Label(search_frame, text="🔍", bg=SECONDARY_BG, fg=FG_COLOR, font=("Segoe UI", 16)).pack(side="left", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_courses)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 12))
        search_entry.pack(side="left", fill="x", expand=True, ipady=5)
        
        # Course List Table
        list_frame = tk.Frame(frame, bg=BG_COLOR)
        list_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("ID", "Title", "Skills")
        self.course_tree = ttk.Treeview(list_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set, style="Treeview")
        
        self.course_tree.heading("ID", text="ID")
        self.course_tree.column("ID", width=60, anchor="center")
        self.course_tree.heading("Title", text="Course Title")
        self.course_tree.column("Title", width=300)
        self.course_tree.heading("Skills", text="Related Skills")
        self.course_tree.column("Skills", width=400)
        
        self.course_tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.course_tree.yview)
        
        self.load_courses()

    def load_courses(self):
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        courses = database.get_all_courses()
        for i, course in enumerate(courses):
            # Alternate row colors implicitly by just relying on selection
            self.course_tree.insert("", tk.END, values=course)
            
    def filter_courses(self, *args):
        query = self.search_var.get().lower()
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        courses = database.get_all_courses()
        for course in courses:
            if query in course[1].lower() or query in course[2].lower():
                self.course_tree.insert("", tk.END, values=course)

    def create_rate_frame(self):
        frame = ttk.Frame(self.content_area)
        self.content_frames["Rate"] = frame
        
        self.create_header(frame, "Rate Courses", "Share your feedback to improve your recommendations.")
        
        # Form Container
        form_container = tk.Frame(frame, bg=SECONDARY_BG, padx=40, pady=40)
        form_container.pack(fill="x", padx=40)
        
        tk.Label(form_container, text="Select Course to Rate", font=("Segoe UI", 12, "bold"), fg=FG_COLOR, bg=SECONDARY_BG).pack(anchor="w", pady=(0, 10))
        
        self.rate_course_var = tk.StringVar()
        self.rate_course_dropdown = ttk.Combobox(form_container, textvariable=self.rate_course_var, state="readonly", font=("Segoe UI", 12))
        self.update_rate_dropdown()
        self.rate_course_dropdown.pack(fill="x", pady=(0, 25), ipady=8)
        
        tk.Label(form_container, text="Your Rating (1 to 5 Stars)", font=("Segoe UI", 12, "bold"), fg=FG_COLOR, bg=SECONDARY_BG).pack(anchor="w", pady=(0, 10))
        
        self.rating_var = tk.IntVar(value=5)
        rating_frame = tk.Frame(form_container, bg=SECONDARY_BG)
        rating_frame.pack(anchor="w", pady=(0, 30))
        
        # Star styling via Radiobuttons
        for i in range(1, 6):
            rb = tk.Radiobutton(rating_frame, text=f"{i} ⭐", variable=self.rating_var, value=i, 
                                font=("Segoe UI", 12, "bold"), bg=SECONDARY_BG, fg=WARN_COLOR, selectcolor=BG_COLOR,
                                indicatoron=False, width=6, pady=10, borderwidth=2, relief="ridge")
            rb.pack(side="left", padx=(0, 10))
            
        ttk.Button(form_container, text="Submit Rating", style="Primary.TButton", command=self.submit_rating).pack(anchor="w", ipadx=20)

    def update_rate_dropdown(self):
        courses = database.get_all_courses()
        self.rate_course_dropdown["values"] = [f"{c[0]} - {c[1]}" for c in courses]

    def submit_rating(self):
        selection = self.rate_course_var.get()
        if not selection:
            messagebox.showerror("Error", "Please select a course.")
            return
            
        course_id = int(selection.split(" - ")[0])
        rating = self.rating_var.get()
        
        database.add_rating(self.current_user_id, course_id, rating)
        messagebox.showinfo("Success", "Rating saved successfully!")
        self.refresh_my_ratings()
        self.rate_course_dropdown.set('') # reset

    def create_recommendations_frame(self):
        frame = ttk.Frame(self.content_area)
        self.content_frames["Recommendations"] = frame
        
        self.create_header(frame, "Top Picks For You", "AI-driven suggestions based on your interests and peers.")
        
        notebook = ttk.Notebook(frame)
        notebook.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Content-Based Tab
        self.cb_tab = tk.Frame(notebook, bg=BG_COLOR, pady=20)
        notebook.add(self.cb_tab, text="   🎯 Content-Based   ")
        
        # Collaborative Tab
        self.cf_tab = tk.Frame(notebook, bg=BG_COLOR, pady=20)
        notebook.add(self.cf_tab, text="   🤝 Collaborative   ")

    def create_course_card(self, parent, title, subtitle, badge_text, badge_color):
        card = tk.Frame(parent, bg=SECONDARY_BG, padx=20, pady=15)
        card.pack(fill="x", pady=8)
        
        info_frame = tk.Frame(card, bg=SECONDARY_BG)
        info_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(info_frame, text=title, font=("Segoe UI", 16, "bold"), fg=FG_COLOR, bg=SECONDARY_BG).pack(anchor="w")
        tk.Label(info_frame, text=subtitle, font=("Segoe UI", 11), fg=TEXT_COLOR, bg=SECONDARY_BG).pack(anchor="w", pady=(5, 0))
        
        badge_frame = tk.Frame(card, bg=badge_color, padx=12, pady=6)
        badge_frame.pack(side="right")
        tk.Label(badge_frame, text=badge_text, font=("Segoe UI", 12, "bold"), fg=BG_COLOR, bg=badge_color).pack()

    def load_recommendations(self):
        # Clear existing
        for widget in self.cb_tab.winfo_children():
            widget.destroy()
        for widget in self.cf_tab.winfo_children():
            widget.destroy()
            
        user = database.get_user(self.current_user_id)
        if not user: return
        interest = user[2]
        
        # Header for CB
        tk.Label(self.cb_tab, text=f"Based on your interest in: {interest}", font=("Segoe UI", 12, "italic"), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(0, 15))
        
        # Load Content-Based
        cb_recs = recommend_content(interest)
        if cb_recs:
            for title, skills, score in cb_recs:
                self.create_course_card(self.cb_tab, title, f"Skills: {skills}", f"{score}% Match", SUCCESS_COLOR)
        else:
            tk.Label(self.cb_tab, text="No exact matches found. Try broadening your interests.", fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)
            
        # Header for CF
        tk.Label(self.cf_tab, text="Courses highly rated by students similar to you", font=("Segoe UI", 12, "italic"), fg=TEXT_COLOR, bg=BG_COLOR).pack(anchor="w", pady=(0, 15))
        
        # Load Collaborative
        cf_recs = recommend_collab(self.current_user_id)
        if cf_recs:
            for cid, title, avg_rating in cf_recs:
                self.create_course_card(self.cf_tab, title, f"Course ID: {cid}", f"⭐ {avg_rating}/5.0", WARN_COLOR)
        else:
            empty_msg = "Not enough activity data to find similar users yet.\nRate some courses first to unlock collaborative recommendations!"
            tk.Label(self.cf_tab, text=empty_msg, fg=TEXT_COLOR, bg=BG_COLOR, justify="center").pack(pady=40)

    def create_my_ratings_frame(self):
        frame = ttk.Frame(self.content_area)
        self.content_frames["MyRatings"] = frame
        
        self.create_header(frame, "My Ratings", "Manage the courses you've rated.")
        
        list_frame = tk.Frame(frame, bg=BG_COLOR)
        list_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("Course ID", "Title", "Rating")
        self.ratings_tree = ttk.Treeview(list_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set, style="Treeview")
        
        self.ratings_tree.heading("Course ID", text="Course ID")
        self.ratings_tree.column("Course ID", width=100, anchor="center")
        self.ratings_tree.heading("Title", text="Title")
        self.ratings_tree.column("Title", width=450)
        self.ratings_tree.heading("Rating", text="Your Rating")
        self.ratings_tree.column("Rating", width=150, anchor="center")
        
        self.ratings_tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.ratings_tree.yview)
        
        btn_frame = tk.Frame(frame, bg=BG_COLOR)
        btn_frame.pack(pady=(0, 40), padx=40, anchor="e")
        ttk.Button(btn_frame, text="🗑️ Delete Selected Rating", command=self.delete_selected_rating, style="Primary.TButton").pack()

    def refresh_my_ratings(self):
        for item in self.ratings_tree.get_children():
            self.ratings_tree.delete(item)
        ratings = database.get_user_ratings(self.current_user_id)
        for r in ratings:
            star_rating = "⭐" * r[3]
            self.ratings_tree.insert("", tk.END, values=(r[0], r[1], star_rating))

    def delete_selected_rating(self):
        selected = self.ratings_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a rating to delete from the table.")
            return
            
        item = self.ratings_tree.item(selected[0])
        course_id = item['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this rating?"):
            database.delete_rating(self.current_user_id, course_id)
            self.refresh_my_ratings()

    def show_browse_frame(self):
        self.show_content_frame("Browse")
        
    def show_rate_frame(self):
        self.update_rate_dropdown()
        self.show_content_frame("Rate")
        
    def show_recommendations_frame(self):
        self.load_recommendations()
        self.show_content_frame("Recommendations")
        
    def show_my_ratings_frame(self):
        self.refresh_my_ratings()
        self.show_content_frame("MyRatings")

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.place_forget()
        self.frames[frame_name].place(relwidth=1, relheight=1)

    def logout(self):
        self.current_user_id = None
        self.current_user_name = None
        self.update_user_dropdown()
        self.new_name_var.set("Enter your name")
        self.new_interest_var.set("Main interest (e.g., Python)")
        self.show_frame("LoginFrame")

if __name__ == "__main__":
    app = EarningApp()
    app.mainloop()
