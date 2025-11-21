# 📘 Dark VizMate - Text to Diagram Conversion Manual

## 🎯 Purpose
This manual helps you convert your existing text documents, flowcharts, or process descriptions into the format accepted by Dark VizMate diagram generator.

---

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Format Rules](#format-rules)
3. [Step-by-Step Conversion Guide](#step-by-step-conversion-guide)
4. [Common Patterns](#common-patterns)
5. [VS Code Workflow](#vs-code-workflow)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Using VS Code (Recommended)

1. **Open VS Code**
   - Install VS Code if you don't have it: https://code.visualstudio.com/

2. **Open Your File**
   - File → Open File (or `Ctrl+O` / `Cmd+O`)
   - Select your document (text file, markdown, etc.)

3. **Open This Manual**
   - File → Open File
   - Open `CONVERSION_MANUAL.md` (this file)

4. **Split View**
   - Right-click on one tab → "Split Right"
   - Now you have both files side-by-side

5. **Convert Your Text**
   - Follow the format rules below
   - Use Find & Replace (`Ctrl+H` / `Cmd+H`) for bulk conversions
   - Copy the converted text

6. **Paste in Dark VizMate**
   - Go to Dark VizMate app
   - Paste your converted text
   - Generate diagram!

---

## 📐 Format Rules

### 1. Cluster/Section Titles
**Format:** `## Title Name`

**Examples:**
```
## Authentication Flow
## API Layer
## Database Operations
```

**Conversion Tips:**
- If your document has headings like "Step 1:", "Phase 1:", "Section A:" → Convert to `## Step 1`, `## Phase 1`, `## Section A`
- If you have numbered lists, you can group them: `## Process Steps`

---

### 2. Horizontal Flow (Left to Right)
**Format:** `Node A → Node B → Node C`

**Alternatives:**
- `Node A -> Node B -> Node C`
- `Node A => Node B => Node C`

**Conversion Tips:**
- "then" → `→`
- "followed by" → `→`
- "goes to" → `→`
- "leads to" → `→`
- "next" → `→`

**Examples:**
```
Original: "User logs in, then enters credentials, then submits form"
Converted: User Logs In → Enter Credentials → Submit Form

Original: "Request goes to API, which processes it, then returns response"
Converted: Request → API [Process] → Return Response
```

---

### 3. Vertical Flow (Top to Bottom)
**Format:** Use `↓` on a separate line

**Alternatives:**
- `v` (lowercase v)
- `|` (pipe character)

**Conversion Tips:**
- "after that" → `↓`
- "then" (when starting new line) → `↓`
- "subsequently" → `↓`
- Line breaks in your document → `↓`

**Examples:**
```
Original:
Step 1: User clicks button
Step 2: System validates input
Step 3: System processes request

Converted:
User Clicks Button
↓
System Validates Input
↓
System Processes Request
```

---

### 4. Edge Labels (Connection Descriptions)
**Format:** `Node A [Label Text] → Node B`

**Conversion Tips:**
- "via", "using", "through" → `[via Method]`
- HTTP methods → `[GET]`, `[POST]`, `[PUT]`, `[DELETE]`
- Actions → `[Validate]`, `[Process]`, `[Store]`
- Conditions → `[If Valid]`, `[On Success]`, `[On Error]`

**Examples:**
```
Original: "Client sends GET request to API"
Converted: Client [GET] → API

Original: "User authenticates using OAuth"
Converted: User [OAuth] → Authentication Service

Original: "If validation succeeds, proceed to next step"
Converted: Validation [If Success] → Next Step
```

---

## 🔄 Step-by-Step Conversion Guide

### Step 1: Identify Your Flow Structure
- **Linear Flow**: A → B → C → D
- **Branching Flow**: A → B → C (success) OR A → B → D (failure)
- **Hierarchical Flow**: Main → Sub-process 1, Sub-process 2, Sub-process 3
- **Loop Flow**: A → B → C → (back to) A

### Step 2: Extract Key Nodes
- Identify all the main steps, processes, or components
- Write them as simple, clear names
- Remove unnecessary words: "the", "a", "an", "is", "are"

**Example:**
```
Original: "The user is required to enter their username and password"
Extracted: "Enter Username and Password"
```

### Step 3: Identify Connections
- Find how nodes connect to each other
- Determine direction (horizontal or vertical)
- Note any conditions or labels on connections

### Step 4: Group Related Steps
- Use `## Cluster Title` to group related processes
- This creates visual sections in your diagram

### Step 5: Add Edge Labels
- Add `[label]` to connections that need description
- Keep labels short and clear

### Step 6: Test Your Format
- Copy your converted text
- Paste into Dark VizMate
- Check if diagram looks correct
- Adjust as needed

---

## 🎨 Common Patterns

### Pattern 1: Simple Linear Process
```
## Process Name
Step 1 → Step 2 → Step 3 → Step 4
```

### Pattern 2: Decision Flow
```
## Decision Flow
Start → Check Condition
↓
Condition [If True] → Path A → End
Condition [If False] → Path B → End
```

### Pattern 3: API Request-Response
```
## API Flow
Client → API Gateway [Request]
↓
API Gateway → Backend Service [Process]
↓
Backend Service → Database [Query]
↓
Database → Backend Service [Data]
↓
Backend Service → API Gateway [Response]
↓
API Gateway → Client [JSON]
```

### Pattern 4: Multi-Layer Architecture
```
## Frontend
Browser → React App → API Client
↓
## Backend
API Client → REST API → Business Logic
↓
## Data Layer
Business Logic → Database → Storage
```

### Pattern 5: Error Handling
```
## Main Flow
Start → Process → Validate
↓
Validate [Success] → Continue → End
Validate [Error] → Error Handler → Log Error → End
```

---

## 💻 VS Code Workflow

### Setup
1. Open VS Code
2. Install extensions (optional but helpful):
   - **Markdown Preview Enhanced** - For viewing markdown
   - **Multi-cursor** - For bulk editing

### Conversion Workflow

#### Method 1: Manual Conversion
1. Open your source file
2. Open `CONVERSION_MANUAL.md` (split view)
3. Read your source file line by line
4. Convert each section following the rules
5. Create a new file: `converted_diagram.txt`
6. Paste converted content
7. Copy and use in Dark VizMate

#### Method 2: Find & Replace (Bulk Conversion)
1. Open your source file
2. Press `Ctrl+H` (Windows/Linux) or `Cmd+H` (Mac)
3. Use these common replacements:

| Find | Replace With | Notes |
|------|--------------|-------|
| ` then ` | ` → ` | Space before and after |
| ` goes to ` | ` → ` | |
| ` followed by ` | ` → ` | |
| `Step 1:` | `## Step 1` | For numbered steps |
| `Phase 1:` | `## Phase 1` | For phases |
| `\n\n` | `\n↓\n` | Double line breaks → vertical flow |

4. Review and adjust manually
5. Copy to Dark VizMate

#### Method 3: Using Multi-Cursor
1. Select similar patterns (e.g., all "Step X:")
2. Press `Alt+Click` (Windows/Linux) or `Cmd+Click` (Mac) to add cursors
3. Type your replacement
4. All instances update simultaneously

---

## 📚 Examples

### Example 1: Converting a Process Document

**Original Document:**
```
User Registration Process

1. User visits registration page
2. User fills out registration form
3. System validates email format
4. System checks if email exists
5. If email exists, show error
6. If email doesn't exist, create account
7. Send confirmation email
8. Redirect to login page
```

**Converted Format:**
```
## User Registration Process
User Visits Registration Page → Fill Registration Form
↓
System Validates Email Format → Check Email Exists
↓
Email Exists [If Yes] → Show Error
Email Exists [If No] → Create Account → Send Confirmation Email → Redirect to Login
```

### Example 2: Converting an Architecture Description

**Original Document:**
```
System Architecture:

Frontend: React application communicates with REST API
Backend: REST API processes requests and queries PostgreSQL database
Caching: Redis cache stores frequently accessed data
Messaging: RabbitMQ handles asynchronous message processing
```

**Converted Format:**
```
## Frontend Layer
React App → REST API
↓
## Backend Layer
REST API → Business Logic → PostgreSQL Database
↓
## Caching Layer
Business Logic → Redis Cache
↓
## Messaging Layer
Business Logic → RabbitMQ → Message Processing
```

### Example 3: Converting a Flowchart Description

**Original Document:**
```
Login Flow:
- User enters credentials
- System validates credentials against database
- If valid: generate session token and redirect to dashboard
- If invalid: show error message and return to login
```

**Converted Format:**
```
## Login Flow
User Enters Credentials → System Validates Credentials
↓
System Validates Credentials → Database [Check]
↓
Database [Valid] → Generate Session Token → Redirect to Dashboard
Database [Invalid] → Show Error Message → Return to Login
```

---

## 🔧 Troubleshooting

### Problem: Diagram doesn't show connections
**Solution:** Make sure you're using `→`, `->`, or `=>` between nodes

### Problem: Nodes appear in wrong order
**Solution:** Check your flow direction. Use `↓` for vertical flow

### Problem: Clusters not appearing
**Solution:** Ensure cluster titles start with `## ` (two hashes and a space)

### Problem: Edge labels not showing
**Solution:** Format should be `Node A [Label] → Node B` with square brackets

### Problem: Too many nodes in one line
**Solution:** Break into multiple lines using `↓` for vertical flow

### Problem: Special characters causing issues
**Solution:** Avoid using `<`, `>`, `{`, `}` in node names. Use simple text.

---

## 💡 Pro Tips

1. **Start Simple**: Begin with a basic flow, then add complexity
2. **Use Descriptive Names**: Clear node names make better diagrams
3. **Group Related Steps**: Use clusters to organize your diagram
4. **Test Frequently**: Paste into Dark VizMate often to see results
5. **Keep It Readable**: Don't make lines too long (max 3-4 nodes per line)
6. **Use Edge Labels**: They add valuable context to connections
7. **Iterate**: Your first conversion might not be perfect - refine it!

---

## 📞 Need Help?

1. Check the **Syntax Guide** in Dark VizMate app
2. Download the **Sample Format File** for examples
3. Review the examples in this manual
4. Start with simple flows and build complexity gradually

---

## ✅ Quick Checklist

Before pasting into Dark VizMate, verify:
- [ ] All cluster titles start with `## `
- [ ] All connections use `→`, `->`, or `=>`
- [ ] Vertical flows use `↓` on separate lines
- [ ] Edge labels are in square brackets: `[label]`
- [ ] Node names are clear and concise
- [ ] No special characters that might break parsing
- [ ] Flow direction makes logical sense

---

**Happy Diagramming! 🎨**

*Last Updated: 2024*

