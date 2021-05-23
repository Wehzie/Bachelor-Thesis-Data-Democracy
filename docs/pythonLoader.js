async function readPyArgs() {
    const months = document.getElementById("months").value
    const runs = document.getElementById("runs").value
    const gov = document.getElementById("gov").value
    const f = document.getElementById("f").value
    const hh = document.getElementById("hh").value

    const args = ["--months", months, "--runs", runs, "--gov", gov, "--f", f, "--hh", hh]
    return args
}

async function feedbackLoadPackages() {
    addToOutput("Initializing Pyodide.")
    await loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v0.17.0/full/" })
    addToOutput("Done loading Pyodide!")
    addToOutput("Loading Python packages. This may take a while the first time!")
    await pyodide.loadPackage('matplotlib')
    await pyodide.loadPackage('scipy')
    addToOutput("Done loading packages!")
}

function addToOutput(s) {
    text_output.value += "\n" + s
    text_output.scrollTop = text_output.scrollHeight // scroll to bottom
}

async function evaluatePython() {
    window.args = await readPyArgs()
    
    const joint_src = (
        await py_import() +
        await gov_dir() +
        await gov_rep() +
        await firm() +
        await household() +
        await simulation() +
        await statistician() +
        await stat_run() +
        await stat_runs() +
        await main() +
        (`
import js
from js import args

# pass arguments
sys.argv.extend(args.to_py())

main()
        `)
    )
    console.log(joint_src)

    addToOutput("Proceeding to run the simulation.\n")
    try {
        await pyodide.runPythonAsync(joint_src)
        addToOutput("Ran the simulation.\n")
    } catch (err) {
        addToOutput(err)
        addToOutput("Could not run the simulation!\n")
    }
}

window.onload = feedbackLoadPackages