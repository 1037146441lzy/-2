# Smart Research Assistant Agent

## Introduction

This project implements a Smart Research Assistant Agent based on Qwen.

The agent can:

- Search information from Internet
- Query current weather
- Query current time
- Maintain conversation context

## Skills

### Tool 1: search_web

Search real-time information.

### Tool 2: get_weather

Get weather information.

### Tool 3: get_current_time

Get current system time.

## Context Integration

Conversation history is stored in a messages list.

The entire conversation history is sent to the LLM in every request.

## Architecture

User
↓
Qwen LLM
↓
Function Calling
↓
Tools
(search / weather / time)

## Installation

pip install -r requirements.txt

## Run

python main.py

## Prompt

See prompts.py
