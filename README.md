# Library-Management-System
Here I have build a Library management that is build upon Python and it is using a SQL database in MySQL workbench to store manage the data.

A GUI-based Library Management System built using **Python (Tkinter)** for the frontend and **MySQL** for the backend database operations.

## Overview
This project provides a fully functional Library Management System with a **user-friendly GUI** for managing library members, borrowed books, and book details. The system automates the tracking of borrowed books, due dates, and overdue fines, reducing manual workload for library staff.

Key functionalities include **CRUD operations**, a **calendar widget for selecting borrowed dates**, and a **Treeview table to display records**.

## Features
- Add Library Members: Register new members with personal details.
- Borrow Books: Track borrowed books, due dates, and overdue status.
- Search Records: Search library members by their reference ID.
- Delete Records: Remove library member records from the database.
- Reset Forms: Clear all input fields for new entries.
- Calendar Integration: Select borrowed date using a calendar widget.
- Treeview Table: Display all library records in a tabular format.
- Pre-loaded Books: Sample book data with ISBN, author, and loan period.
- Automatic Calculations: Auto-calculate due dates and overdue status.

## Technologies Used
- Python 3.x
- Tkinter – GUI development
- tkcalendar – Calendar widget integration
- MySQL – Backend database
- pymysql – Python MySQL connector

## Installation

git clone https://github.com/<your-username>/LibraryManagementSystem.git
cd LibraryManagementSystem

pip install tk tkcalendar pymysql


CREATE DATABASE librarymanagementsysytem;
USE librarymanagementsysytem;

CREATE TABLE library(
    member VARCHAR(20),
    firstname VARCHAR(50),
    surname VARCHAR(50),
    address VARCHAR(100),
    dateborrowed DATE,
    datedue DATE,
    dayoverdue VARCHAR(20),
    author VARCHAR(50),
    bookisbn VARCHAR(50),
    booktitle VARCHAR(50)
);

sqlCon = pymysql.connect(
    host="localhost",
    user="root",
    password="root1216",
    database="librarymanagementsysytem"
)

Use the GUI to:

Add member and book details.

Select a book from the list to auto-fill details.

Choose the borrowed date using the calendar widget.

Display, search, or delete records.

Reset input fields using the "Reset" button.

Database Schema

Table: library

Column	Type	Description
member	VARCHAR(20)	Member Reference Number

firstname	VARCHAR(50)	First Name of the Member

surname	VARCHAR(50)	Surname

address	VARCHAR(100)	Member Address

dateborrowed	DATE	Book Borrowed Date

datedue	DATE	Due Date

dayoverdue	VARCHAR(20)	Overdue Status

author	VARCHAR(50)	Author of the Book

bookisbn	VARCHAR(50)	Book ISBN

booktitle	VARCHAR(50)	Book Title


Author

Debarka Das
College: National Institute of Technology, Warangal
