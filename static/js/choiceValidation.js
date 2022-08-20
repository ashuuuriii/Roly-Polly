"use strict";

const form = document.querySelector("form");

function stringToDate(str) {
  if (str.length < 1) return;

  const dateSplit = str.split(" ");
  const daysSplit = dateSplit[0].split("/");
  const timeSplit = dateSplit[1].split(":");

  return new Date(
    daysSplit[2], // year
    daysSplit[1] - 1, // month index [0-11]
    daysSplit[0], // day
    timeSplit[0], // hour
    timeSplit[1] // minute
  );
}

function checkChoicesExist(e, choices) {
  let nValidChoices = 0;
  const errorBox = document.querySelector("#error-top");
  for (let choice of choices) {
    const deleted = document.querySelector(
      `#id_form-${choice.id.replace(/[^0-9]/g, "")}-DELETE`
    ).checked;
    if (choice.value.length > 0 && !deleted) {
      nValidChoices++;
    }
  }
  if (nValidChoices < 1) {
    e.preventDefault();
    errorBox.textContent =
      "You cannot create a new event without any event times.";
    return false;
  } else {
    errorBox.textContent = "";
    return true;
  }
}

function checkChoiceValuesAreValid(e, choices) {
  let isValid = true;

  for (let choice of choices) {
    const formN = choice.id.replace(/[^0-9]/g, "");
    const deleted = document.querySelector(`#id_form-${formN}-DELETE`).checked;
    const timeTo = document.querySelector(`#id_form-${formN}-time_to`);
    const errorBox = document.querySelector(`#error-${formN}`);
    const timeFromVal = stringToDate(choice.value);
    const timeToVal = stringToDate(timeTo.value);
    const now = new Date();

    if (deleted) {
      continue;
    } else if (!timeFromVal && timeToVal) {
      choice.style = "border-color: var(--red);";
      errorBox.textContent = "Start time is required.";
      isValid = false;
    } else if (
      (timeFromVal && timeFromVal < now) ||
      (timeToVal && timeToVal < now)
    ) {
      errorBox.textContent = "Event times must not be in the past.";
      isValid = false;
    } else if (timeFromVal >= timeToVal) {
      timeTo.style = "border-color: var(--red);";
      errorBox.textContent = "Finish time must be after start time.";
      isValid = false;
    } else {
      timeTo.style = "border-color: var(--contrast-dark);";
      choice.style = "border-color: var(--contrast-dark);";
      errorBox.textContent = "";
    }
  }

  if (!isValid) e.preventDefault();
}

function validateChoicesOnSubmit(e) {
  let isValid;
  const choices = document.querySelectorAll('input[id$="time_from"]');
  isValid = checkChoicesExist(e, choices);
  if (isValid) checkChoiceValuesAreValid(e, choices);
}

form.addEventListener("submit", (e) => validateChoicesOnSubmit(e));
