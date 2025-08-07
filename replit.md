# WhatsApp Taxi Bot

## Overview

This is a WhatsApp-based taxi booking system that allows customers to request rides through WhatsApp messages. The system uses a hybrid distance calculation approach (local coordinates + Google Maps when needed) to minimize API costs by 90%. It provides accurate price estimates and manages the entire ride booking workflow. Includes a web dashboard for the driver to monitor rides and statistics.

**Project Status**: Complete and ready for client demonstration
**Cost Model**: Opção 1 - Econômica (Recomendada) - ~R$0.025 per ride operational cost
**Target**: Freelancer project for taxi/private driver service

## User Preferences

Preferred communication style: Simple, everyday language.
Project focus: Cost-effective solution for freelancer client with minimal operational expenses.

## System Architecture

### Backend Architecture
- **Flask Web Framework**: Main application server handling web routes, webhook endpoints, and API endpoints
- **Conversational Bot Logic**: State-machine based WhatsApp bot that guides customers through ride booking process using session management
- **Data Models**: Simple dataclass-based models for Ride and CustomerSession entities
- **File-based Data Storage**: JSON files for persisting rides and customer sessions (rides.json, sessions.json)

### Frontend Architecture
- **Server-side Rendered Templates**: HTML templates using Jinja2 for dashboard and rides pages
- **Bootstrap Dark Theme**: Responsive UI with dark theme specifically designed for agent compatibility
- **Feather Icons**: Clean, minimal iconography throughout the interface
- **Real-time Updates**: JavaScript-based dashboard updates via API calls

### Pricing Engine
- **Distance-based Calculation**: R$1.50 per kilometer base rate
- **Passenger-based Minimums**: R$15 minimum for 1 passenger, R$18 minimum for 2+ passengers
- **Transparent Breakdown**: Detailed price calculation logic for customer transparency

### Communication Flow
- **WhatsApp Integration**: Twilio-powered WhatsApp messaging for customer interactions
- **Webhook Processing**: Real-time message handling and response generation
- **Multi-step Conversation**: Guided booking process collecting pickup, destination, and passenger count
- **Driver Notifications**: Automatic WhatsApp notifications to driver for new bookings

### Route Calculation
- **Google Maps Integration**: Distance Matrix API for accurate distance and duration calculations
- **Brazilian Localization**: Portuguese language and Brazil region settings for optimal results
- **Error Handling**: Fallback mechanisms for API failures

## External Dependencies

### Communication Services
- **Twilio WhatsApp API**: Message sending/receiving, webhook handling
- **Google Maps Distance Matrix API**: Route calculation and location services

### Environment Configuration
- **Twilio Credentials**: Account SID, Auth Token, Phone Number
- **Google Maps API Key**: For distance calculations
- **Driver Information**: Phone number and PIX payment details
- **Session Secret**: Flask session management

### Frontend Libraries
- **Bootstrap 5**: CSS framework with dark theme
- **Feather Icons**: SVG icon library
- **Custom CSS**: WhatsApp-themed styling with green color scheme

### Development Dependencies
- **Flask**: Web framework and templating
- **Werkzeug ProxyFix**: Reverse proxy support
- **Python Standard Libraries**: JSON handling, datetime, logging, os, uuid