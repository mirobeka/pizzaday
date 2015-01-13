#!/bin/bash

case "$1" in
        developing)
            export PIZZA_CONFIG=settings.development
            python pizza.py
            ;;
         
        production)
            export PIZZA_CONFIG=settings.production
            python pizza.py
            ;;
         
        testing)
            export PIZZA_CONFIG=settings.testing
            python pizza_tests.py
            ;;
         
        *)
            echo $"Usage: $0 {developing|testing|production}"
            exit 1
 
esac
