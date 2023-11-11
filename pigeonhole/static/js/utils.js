/**
 * The debounce function is used to limit the number of times a function is called within a specified
 * delay period.
 * @param func - The `func` parameter is the function that you want to debounce. It is the function
 * that will be called after the delay has passed without any further invocations.
 * @param delay - The `delay` parameter is the amount of time in milliseconds that the function should
 * wait before executing.
 * @returns The debounce function returns a new function that will execute the original function (func)
 * after a specified delay (delay) has passed.
 */
export function debounce(func, delay) {
    let timeout;

    return function () {
        const context = this;
        const args = arguments;

        clearTimeout(timeout);

        timeout = setTimeout(() => {
            if (func) {
                func.apply(context, args);
            }
        }, delay);
    };
}