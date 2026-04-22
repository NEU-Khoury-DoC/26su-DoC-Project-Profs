# Handling User Role Access and Control (RBAC)

In most applications, when a user logs in, they assume a particular role in the app. For instance, when one logs in to a stock price prediction app, they may be a single investor, a portfolio manager, or a corporate executive (of a publicly traded company). Each of those *roles* will likely present some similar features as well as some different features when compared to the other roles. This is sometimes called Role-based Access Control, or **RBAC** for short.

The code in this project demonstrates how to implement a simple RBAC system in Streamlit without actually using user authentication (usernames and passwords). The template ships with three example roles — *Political Strategist*, *USAID Worker*, and *System Administrator* — that you will replace with the personas specific to your project.

## Conceptual Overview

When a user "logs in" by clicking a role button on the Home page, two things happen: their role is recorded and they are redirected to that role's landing page. The recording happens in Streamlit's **`session_state`** object.

`session_state` is a dictionary-like object that Streamlit keeps alive for the duration of a user's browser session. Think of it as a small, per-user context bag — any page in the app can read from or write to it, and the values persist as the user navigates between pages. It is the mechanism that lets a page "remember" who is currently using the app.

At login, three keys are written into `session_state`:

| Key | What it holds |
|-----|---------------|
| `authenticated` | `True` — confirms the user has selected a role |
| `role` | A short string identifying the role (e.g. `'administrator'`) |
| `first_name` | A display name used to personalize the UI |

From that point on, every page in the app performs two checks using those values:

1. **Authentication check** — if `authenticated` is not `True` in `session_state`, the page immediately redirects back to `Home.py`. This prevents a user from reaching a page by typing its URL directly.
2. **Navigation check** — a call to `SideBarLinks(...)` reads the `role` from `session_state` and renders only the sidebar links that belong to that role. Users never see links to pages they are not supposed to access.

The result is a lightweight access-control system: roles are set once at login and then silently enforced on every subsequent page load.

## How the Project Template RBAC and Navigation Works

### 1. Disabling the default Streamlit navigation

The standard Streamlit sidebar navigation panel is turned off via `app/src/.streamlit/config.toml`:

```toml
[client]
showSidebarNavigation = false
```

This gives full control over which links appear in the sidebar for each role.

### 2. The navigation module

`app/src/modules/nav.py` contains a set of functions — one per page — that each call `st.sidebar.page_link(...)` to add a single link to the sidebar. Having a separate function per page makes it easy to compose role-specific sidebar menus.

### 3. The Home page and session state

`app/src/Home.py` presents one button per role. When a button is clicked, a few variables are written to Streamlit's `session_state` before redirecting to that role's home page via `st.switch_page(...)`:

| Key | Value |
|-----|-------|
| `authenticated` | `True` |
| `role` | a string identifying the role (e.g. `'pol_strat_advisor'`) |
| `first_name` | a display name for the user |

### 4. Calling SideBarLinks on every page

Near the top of `app/src/Home.py` and every page in `app/src/pages/`, there is a call to `SideBarLinks(...)` from `app/src/modules/nav.py`. This function reads the `role` from `session_state` and renders only the links appropriate for that role.

### 5. Page naming convention

Pages use a two-digit numeric prefix to group them by role:

| Prefix range | Role |
|---|---|
| `00_` – `09_` | Political Strategist |
| `10_` – `19_` | USAID Worker |
| `20_` – `29_` | System Administrator |
| `30_` – `39_` | Shared / all roles |

---

## Adapting RBAC for Your Project

Your team will replace the template roles with the personas relevant to your own project. Here is the recommended sequence of steps.

### Step 1 — Define your personas

Identify the roles your application will support. Every project must include a *System Administrator* role for tasks like retraining the ML model. Beyond that, base your roles on the stakeholders described in your project proposal (e.g., *Researcher*, *NGO Partner*, *Field Officer*).

### Step 2 — Update `Home.py`

For each persona, add a button to `app/src/Home.py`. When clicked, the button should set:

```python
st.session_state['authenticated'] = True
st.session_state['role'] = 'your_role_string'
st.session_state['first_name'] = 'Display Name'
st.switch_page('pages/XX_YourRole_Home.py')
```

Remove the buttons for the template roles you are replacing.

### Step 3 — Update `nav.py`

In `app/src/modules/nav.py`, add a sidebar function for each page your new roles need. Follow the existing pattern:

```python
def your_page_nav():
    st.sidebar.page_link('pages/XX_Your_Page.py', label='Page Label', icon='...')
```

Then update (or add) the role-dispatch block in `SideBarLinks(...)` to call those functions for the appropriate role string.

### Step 4 — Create your pages

Add new page files to `app/src/pages/` using the numbering convention above. Each page should:

1. Call `SideBarLinks(show_home=True)` near the top (after imports).
2. Check `st.session_state.get('authenticated')` and redirect to `Home.py` if the user is not logged in.

### Step 5 — Delete the template pages you don't need

Once your own pages are in place, remove the Political Strategist and USAID Worker example pages that are no longer relevant to your project.
