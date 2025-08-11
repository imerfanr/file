import { GoogleGenAI, Type } from "@google/genai";
import { ScanModule, Finding, IspBlock } from '../types';

const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  throw new Error("API_KEY environment variable not set.");
}

const ai = new GoogleGenAI({ apiKey: API_KEY });

const findingSchema = {
    type: Type.OBJECT,
    properties: {
        id: { type: Type.STRING, description: "A unique string identifier for the finding."},
        timestamp: { type: Type.STRING, description: "An ISO 8601 timestamp string for when the finding was 'discovered'."},
        source: { type: Type.STRING, description: "The name of the module that generated the finding (e.g., 'Nmap Port Scan')."},
        target: { type: Type.STRING, description: "The IP address or identifier of the device related to the finding."},
        severity: { type: Type.STRING, description: "A string: 'Critical', 'High', 'Medium', 'Low', or 'Info'."},
        description: { type: Type.STRING, description: "A concise, one-sentence summary of the finding from the Nmap scan."},
        details: { type: Type.STRING, description: "A more detailed paragraph explaining the finding, its technical implications, and evidence. Should resemble Nmap service version detection output."},
        remediation: { type: Type.STRING, description: "A suggestion on what to do next, such as isolation or physical inspection."},
        latitude: { type: Type.NUMBER, description: "An optional, plausible latitude for the discovered device, within the target city if provided."},
        longitude: { type: Type.NUMBER, description: "An optional, plausible longitude for the discovered device, within the target city if provided."},
    },
    required: ["id", "timestamp", "source", "target", "severity", "description", "details", "remediation"],
};

const analyzeTarget = async (
    target: string,
    modules: ScanModule[],
    addLog: (log: string) => void,
    location?: { province: string, city: string }
): Promise<Finding[]> => {
  const moduleNames = modules.map(m => m.name).join(', ');
  const locationInfo = location ? `The scan is geographically focused on ${location.city}, ${location.province}, Iran. Invent plausible details for this region, referencing local ISPs like 'Asiatech', 'Shatel', or 'Mokhaberat', and generate plausible latitude/longitude coordinates for some findings within that city.` : 'The scan is not tied to a specific geographic location.';
  const minerPorts = "3333,3334,3357,4028,4444,5555,6666,7777,8888,9999,14444,18081,20571";

  const prompt = `
    You are the engine for "MinerHunter AI". Your task is to simulate a hyper-realistic Nmap scan targeting cryptocurrency miners and return the results.

    **Scan Parameters:**
    - **Target:** "${target}"
    - **Nmap Command Simulated:** nmap -sV -p ${minerPorts} --open -T4 ${target}
    - **Active Hunter Modules:** ${moduleNames}
    - **Geographic Focus:** ${locationInfo}

    **Your Simulation Steps:**
    1.  **Simulate Nmap Log:** First, generate a realistic, multi-line log of the Nmap scan process. This should look exactly like the console output of a real Nmap scan. Start with the "Starting Nmap..." line, show host discovery progress, report open ports as they are found, and end with the "Nmap done" summary line.
    2.  **Generate Findings JSON:** Second, based on the *results* of your simulated scan, create a JSON array of finding objects.

    **Key Instructions:**
    - **Nmap Log Realism:** The log must be authentic. Use typical Nmap terminology.
    - **Findings Authenticity:** The JSON findings must directly correspond to the simulated Nmap log. If the log shows port 3333 open with a Stratum service, the JSON must contain a corresponding "Critical" finding.
    - **Device Variety:** The scan should find a mix of devices: some definite miners (e.g., Antminer web interfaces, Stratum protocol), some suspicious devices (e.g., open unknown ports, strange banners), and some benign devices misidentified by the port scan.
    - **Geolocation:** For high-confidence findings in a specified geographic area, invent plausible latitude and longitude coordinates near the city center. For 2-3 findings, you MUST provide coordinates.
    - **Output Format:** The final output MUST be a single JSON object with two keys: "nmapLog" (a single string with newlines) and "findings" (an array of objects adhering to the schema).

    Do not output anything else. The entire response must be this single JSON object.
  `;
  
  try {
    const response = await ai.models.generateContent({
        model: "gemini-2.5-flash",
        contents: prompt,
        config: {
            responseMimeType: "application/json",
            responseSchema: {
                type: Type.OBJECT,
                properties: {
                    nmapLog: { type: Type.STRING },
                    findings: {
                        type: Type.ARRAY,
                        items: findingSchema,
                    }
                },
                required: ["nmapLog", "findings"]
            },
        },
    });

    const jsonText = response.text;
    if (!jsonText) {
        throw new Error("Received an empty response from the API.");
    }
    
    const parsedResponse = JSON.parse(jsonText.trim());

    if (parsedResponse.nmapLog && Array.isArray(parsedResponse.findings)) {
        // Stream the nmap log to the UI
        const logLines = parsedResponse.nmapLog.split('\n');
        for (const line of logLines) {
            addLog(line);
            await new Promise(resolve => setTimeout(resolve, 50)); // simulate typing
        }
        return parsedResponse.findings as Finding[];
    }
    
    throw new Error("API response is not in the expected format of {nmapLog, findings}.");

  } catch (error) {
    console.error("Error during Gemini API call:", error);
    if (error instanceof Error) {
        throw new Error(`Failed to get analysis from Gemini: ${error.message}`);
    }
    throw new Error("An unknown error occurred while contacting the Gemini API.");
  }
};

const getIspBlocksForLocation = async (province: string, city: string): Promise<IspBlock[]> => {
    const prompt = `
    Generate a list of 5 plausible public IP CIDR blocks for major Iranian ISPs in the city of ${city}, ${province}.
    Provide a mix of consumer, business, and mobile network blocks.
    The response MUST be a valid JSON array of objects, strictly adhering to the provided schema. Do not output anything other than the JSON array.
    `;
    try {
        const response = await ai.models.generateContent({
            model: "gemini-2.5-flash",
            contents: prompt,
            config: {
                responseMimeType: "application/json",
                responseSchema: {
                    type: Type.ARRAY,
                    items: {
                        type: Type.OBJECT,
                        properties: {
                            name: { type: Type.STRING, description: "The ISP name, e.g., 'Shatel'" },
                            cidr: { type: Type.STRING, description: "The IP CIDR range, e.g., '92.50.0.0/16'" },
                            description: { type: Type.STRING, description: "A brief description, e.g., 'Business Fiber Block' or 'Residential ADSL'" },
                        },
                        required: ["name", "cidr", "description"],
                    }
                }
            }
        });
        
        const jsonText = response.text;
        if (!jsonText) {
            throw new Error("Received an empty response for ISP blocks.");
        }
        const parsedResponse = JSON.parse(jsonText.trim());
        if (Array.isArray(parsedResponse)) {
            return parsedResponse as IspBlock[];
        }
        throw new Error("ISP Block API response is not in the expected array format.");

    } catch (error) {
        console.error("Error during Gemini ISP Block suggestion call:", error);
        if (error instanceof Error) {
            throw new Error(`Failed to get ISP Blocks from Gemini: ${error.message}`);
        }
        throw new Error("An unknown error occurred while contacting the Gemini API for ISP Blocks.");
    }
};


const suggestIpForLocation = async (province: string, city: string): Promise<string> => {
    const prompt = `
    Based on real-world data, suggest a single, plausible public IP CIDR range for a major consumer or business ISP in the city of ${city}, ${province}, Iran.
    Provide ONLY the CIDR range and nothing else. Example format: 85.133.128.0/20
    `;
    try {
        const response = await ai.models.generateContent({
            model: "gemini-2.5-flash",
            contents: prompt,
        });

        const text = response.text.trim();
        // Basic validation for CIDR format
        if (/^([0-9]{1,3}\.){3}[0-9]{1,3}\/[0-9]{1,2}$/.test(text)) {
            return text;
        } else {
            // Fallback or error
            console.warn("AI did not return a valid CIDR, providing a default.", text);
            return '94.182.0.0/15'; // A plausible fallback for Iran
        }
    } catch (error) {
        console.error("Error during Gemini IP suggestion call:", error);
        if (error instanceof Error) {
            throw new Error(`Failed to get suggestion from Gemini: ${error.message}`);
        }
        throw new Error("An unknown error occurred while contacting the Gemini API for IP suggestion.");
    }
};

export const geminiService = {
  analyzeTarget,
  suggestIpForLocation,
  getIspBlocksForLocation,
};