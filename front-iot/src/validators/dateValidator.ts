import { AbstractControl, FormGroup, FormControl, FormGroupDirective, NgForm, ValidatorFn, ValidationErrors } from '@angular/forms';
import { ErrorStateMatcher } from '@angular/material/core'


export function dateBeforeOfTodayValidator(): ValidatorFn {
    return (control: AbstractControl): {[key: string]: any} | null => {
        const today = new Date();
        const selectedDate = new Date(control.value);
        selectedDate.setDate(selectedDate.getDate() + 1);
        console.log(today)
        if (selectedDate > today) {
        return null; // return null if validation succeeds
        }
        return {'dateBeforeOfToday': {value: control.value}}; // return error object if validation fails
    };
    }

export function timePassedValidator() {
    return (control: AbstractControl): ValidationErrors | null => {
        let [hours, minutes] = (control.value).split(':');
        let currentDate = new Date();
        currentDate.setHours(+hours, +minutes, 0, 0);
        if (currentDate.getTime() <= new Date().getTime()) {
        return { timePassed: true };
        }
        return null;
    };
    }
export function timeFormatValidator( control: AbstractControl): { [key: string]: boolean } | null {
    const regex = /([01]?[0-9]|2[0-3]):[0-5][0-9]/;
    if (control.dirty && control.value != '')
        if (control.value !== undefined && !regex.test(control.value)) {
            return { timeFormatError: true };
        }
    return null
    }